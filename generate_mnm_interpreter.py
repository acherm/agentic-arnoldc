#!/usr/bin/env python3
"""Generate an ArnoldC interpreter for MnM Lang programs.

Takes a .mnm file and .mnm.json sidecar, parses the MnM program,
and generates an ArnoldC file that interprets/executes it.

MnM Lang is a stack-based VM with 37 opcodes across 6 color families:
  B (Blue)   = Control flow   (JMP, JZ, JNZ, CALL, RET, HALT)
  G (Green)  = Stack/variables (PUSH, LOAD, STORE, DUP, POP, INC, DEC)
  Y (Yellow) = Arithmetic      (ADD, SUB, MUL, DIV, MOD, EQ, LT, GT)
  O (Orange) = I/O             (PRINT, PRINT_STR, READ_INT, ..., NEWLINE)
  N (Brown)  = Labels/strings  (LABEL, PUSH_STR, CONCAT, LEN, TO_INT, TO_STR)
  R (Red)    = Stack shuffling  (SWAP, ROT, AND, OR, NOT)

Operand encoding: color determines type, value = len(token) - 1.

Usage:
    python3 generate_mnm_interpreter.py prog.mnm prog.mnm.json [output.arnoldc]

Or as a module:
    from generate_mnm_interpreter import generate
    generate(mnm_source, sidecar_dict, output_path="out.arnoldc")
"""

import json
import sys
import os

# ── Internal opcode numbers for the ArnoldC interpreter ──────────────────────

OPCODES = {
    'HALT': 0,
    'NOP': 1,
    'PUSH': 10, 'LOAD': 11, 'STORE': 12, 'DUP': 13,
    'POP': 14, 'INC': 15, 'DEC': 16,
    'ADD': 20, 'SUB': 21, 'MUL': 22, 'DIV': 23, 'MOD': 24,
    'EQ': 25, 'LT': 26, 'GT': 27,
    'JMP': 30, 'JZ': 31, 'JNZ': 32, 'CALL': 33, 'RET': 34,
    'PRINT': 40, 'PRINT_STR': 41, 'READ_INT': 42,
    'READ_STR': 43, 'EMIT_CHAR': 44, 'NEWLINE': 45,
    'SWAP': 50, 'ROT': 51, 'AND': 52, 'OR': 53, 'NOT': 54,
    'PUSH_STR': 60, 'CONCAT': 61, 'LEN': 62, 'TO_INT': 63, 'TO_STR': 64,
}

# ── MnM source decoding tables ──────────────────────────────────────────────

MNM_OPCODES = {
    ('B', 1): 'JMP',   ('B', 2): 'JZ',    ('B', 3): 'JNZ',
    ('B', 4): 'CALL',  ('B', 5): 'RET',   ('B', 6): 'HALT',
    ('G', 1): 'PUSH',  ('G', 2): 'LOAD',  ('G', 3): 'STORE',
    ('G', 4): 'DUP',   ('G', 5): 'POP',   ('G', 6): 'INC',
    ('G', 7): 'DEC',
    ('Y', 1): 'ADD',   ('Y', 2): 'SUB',   ('Y', 3): 'MUL',
    ('Y', 4): 'DIV',   ('Y', 5): 'MOD',   ('Y', 6): 'EQ',
    ('Y', 7): 'LT',    ('Y', 8): 'GT',
    ('O', 1): 'PRINT', ('O', 2): 'PRINT_STR', ('O', 3): 'READ_INT',
    ('O', 4): 'READ_STR', ('O', 5): 'EMIT_CHAR', ('O', 6): 'NEWLINE',
    ('N', 1): 'LABEL', ('N', 2): 'PUSH_STR', ('N', 3): 'CONCAT',
    ('N', 4): 'LEN',   ('N', 5): 'TO_INT',  ('N', 6): 'TO_STR',
    ('R', 1): 'SWAP',  ('R', 2): 'ROT',   ('R', 3): 'AND',
    ('R', 4): 'OR',    ('R', 5): 'NOT',
}

# ── Parsing ──────────────────────────────────────────────────────────────────

def parse_mnm(source):
    """Parse MnM source into list of (opcode_name, operand_value|None)."""
    instructions = []
    for line in source.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        tokens = line.split()
        opcode_token = tokens[0]
        color = opcode_token[0]
        length = len(opcode_token)
        key = (color, length)
        if key not in MNM_OPCODES:
            raise ValueError(f"Unknown opcode token: {opcode_token!r}")
        opcode_name = MNM_OPCODES[key]
        operand_value = None
        if len(tokens) > 1:
            operand_value = len(tokens[1]) - 1
        instructions.append((opcode_name, operand_value))
    return instructions


def resolve_labels(instructions):
    """Resolve label references to instruction indices.

    LABEL becomes NOP at runtime.  JMP/JZ/JNZ/CALL operands are replaced
    with the target instruction index.

    Returns (resolved_instructions, label_map).
    """
    label_map = {}
    for i, (op, operand) in enumerate(instructions):
        if op == 'LABEL':
            label_map[operand] = i
    resolved = []
    for op, operand in instructions:
        if op in ('JMP', 'JZ', 'JNZ', 'CALL'):
            if operand not in label_map:
                raise ValueError(f"Undefined label: {operand}")
            resolved.append((op, label_map[operand]))
        elif op == 'LABEL':
            resolved.append(('NOP', operand if operand is not None else 0))
        else:
            resolved.append((op, operand))
    return resolved, label_map


def estimate_stack_size(instructions):
    """Conservative estimate of maximum stack depth."""
    depth = 0
    max_depth = 0
    for op, _ in instructions:
        if op in ('PUSH', 'LOAD', 'DUP', 'READ_INT', 'PUSH_STR', 'READ_STR'):
            depth += 1
        elif op in ('POP', 'PRINT', 'STORE', 'EMIT_CHAR'):
            depth -= 1
        elif op in ('ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'EQ', 'LT', 'GT',
                     'AND', 'OR', 'CONCAT'):
            depth -= 1   # pop 2, push 1
        elif op in ('JZ', 'JNZ'):
            depth -= 1
        max_depth = max(max_depth, depth)
    return max(max_depth + 5, 10)


# ── Code generation ──────────────────────────────────────────────────────────

def generate(mnm_source, sidecar_data, output_path=None,
             stack_size=None, call_stack_size=None):
    """Generate ArnoldC source that interprets the given MnM program.

    Args:
        mnm_source:     MnM source text.
        sidecar_data:   Parsed sidecar JSON dict.
        output_path:    Where to write the .arnoldc file (optional).
        stack_size:     Max stack depth (auto-estimated if None).
        call_stack_size: Max call nesting (default 5).

    Returns:
        Generated ArnoldC source as a string.
    """
    raw = parse_mnm(mnm_source)
    instructions, label_map = resolve_labels(raw)

    num_vars = len(sidecar_data.get('variables', []))
    var_init = sidecar_data.get('variables', [])
    strings = sidecar_data.get('strings', [])
    int_queues = sidecar_data.get('inputs', {}).get('int', [])
    num_queues = len(int_queues)

    if stack_size is None:
        stack_size = estimate_stack_size(instructions)
    if call_stack_size is None:
        call_stack_size = 5

    # Encode instructions as integer pairs
    enc_op = []
    enc_arg = []
    for op, operand in instructions:
        enc_op.append(OPCODES[op])
        enc_arg.append(operand if operand is not None else 0)
    prog_size = len(enc_op)

    lines = []
    def emit(s=""):
        lines.append(s)

    # Helper strings for method calls
    s_args = " ".join(f"s{i}" for i in range(stack_size))
    v_args = " ".join(f"v{i}" for i in range(num_vars)) if num_vars else ""
    cs_args = " ".join(f"cs{i}" for i in range(call_stack_size))

    # ═══════════════════════════════════════════════════════════════════════
    # A.  MAIN PROGRAM — variable declarations
    # ═══════════════════════════════════════════════════════════════════════
    emit("IT'S SHOWTIME")
    emit()

    # Stack cells
    for i in range(stack_size):
        emit(f"HEY CHRISTMAS TREE s{i}")
        emit("YOU SET US UP 0")
    emit()

    # MnM variables
    for i in range(num_vars):
        val = var_init[i] if i < len(var_init) else 0
        emit(f"HEY CHRISTMAS TREE v{i}")
        emit(f"YOU SET US UP {val}")
    emit()

    # Call stack
    for i in range(call_stack_size):
        emit(f"HEY CHRISTMAS TREE cs{i}")
        emit("YOU SET US UP 0")
    emit()

    # Input-queue pointers (one per queue)
    for qi in range(num_queues):
        emit(f"HEY CHRISTMAS TREE iqp{qi}")
        emit("YOU SET US UP 0")
    emit()

    # Control variables
    ctrl = [
        ("ip", 0), ("sp", 0), ("csp", 0), ("running", 1),
        ("opcode", 0), ("operand", 0),
        ("a", 0), ("b", 0), ("c", 0), ("result", 0),
        ("isOp", 0), ("jumped", 0), ("notJumped", 0), ("spTmp", 0),
        ("dummy", 0),
    ]
    for name, val in ctrl:
        emit(f"HEY CHRISTMAS TREE {name}")
        emit(f"YOU SET US UP {val}")
    emit()

    # ═══════════════════════════════════════════════════════════════════════
    # B.  MAIN EXECUTION LOOP
    # ═══════════════════════════════════════════════════════════════════════
    emit("STICK AROUND running")
    emit()

    # B1. Fetch instruction
    emit("GET YOUR ASS TO MARS opcode")
    emit("DO IT NOW fetchOpcode ip")
    emit("GET YOUR ASS TO MARS operand")
    emit("DO IT NOW fetchOperand ip")
    emit()

    # Reset jumped flag
    emit("GET TO THE CHOPPER jumped")
    emit("HERE IS MY INVITATION 0")
    emit("ENOUGH TALK")
    emit()

    # ── helper closures for repetitive patterns ──────────────────────────

    def emit_check_opcode(opcode_name):
        """Emit:  isOp = (opcode == CODE)  +  if-open."""
        emit("GET TO THE CHOPPER isOp")
        emit("HERE IS MY INVITATION opcode")
        emit(f"YOU ARE NOT YOU YOU ARE ME {OPCODES[opcode_name]}")
        emit("ENOUGH TALK")
        emit("BECAUSE I'M GOING TO SAY PLEASE isOp")

    def emit_end_if():
        emit("YOU HAVE NO RESPECT FOR LOGIC")

    def emit_stack_push_a():
        """Write variable 'a' to stack[sp], then sp++."""
        for i in range(stack_size):
            emit(f"GET YOUR ASS TO MARS s{i}")
            emit(f"DO IT NOW condWrite sp {i} s{i} a")
        emit("GET TO THE CHOPPER sp")
        emit("HERE IS MY INVITATION sp")
        emit("GET UP 1")
        emit("ENOUGH TALK")

    def emit_stack_pop_into(var):
        """sp--, read stack[sp] into var."""
        emit("GET TO THE CHOPPER sp")
        emit("HERE IS MY INVITATION sp")
        emit("GET DOWN 1")
        emit("ENOUGH TALK")
        emit(f"GET YOUR ASS TO MARS {var}")
        emit(f"DO IT NOW stackRead sp {s_args}")

    def emit_stack_write_at(idx_var, val_var):
        """Write val_var to stack[idx_var] (all cells)."""
        for i in range(stack_size):
            emit(f"GET YOUR ASS TO MARS s{i}")
            emit(f"DO IT NOW condWrite {idx_var} {i} s{i} {val_var}")

    def emit_var_write_a():
        """Write 'a' to variable[operand]."""
        for i in range(num_vars):
            emit(f"GET YOUR ASS TO MARS v{i}")
            emit(f"DO IT NOW condWrite operand {i} v{i} a")

    def emit_set_jump():
        """ip = operand; jumped = 1"""
        emit("GET TO THE CHOPPER ip")
        emit("HERE IS MY INVITATION operand")
        emit("ENOUGH TALK")
        emit("GET TO THE CHOPPER jumped")
        emit("HERE IS MY INVITATION 1")
        emit("ENOUGH TALK")

    # B2. Opcode dispatch ─────────────────────────────────────────────────

    # ── HALT ─────────────────────────────────────────────────────────────
    emit_check_opcode('HALT')
    emit("GET TO THE CHOPPER running")
    emit("HERE IS MY INVITATION 0")
    emit("ENOUGH TALK")
    emit_end_if()
    emit()

    # ── NOP (LABEL at runtime) — nothing to do ──────────────────────────

    # ── PUSH ─────────────────────────────────────────────────────────────
    emit_check_opcode('PUSH')
    # Write operand to stack[sp] then sp++
    for i in range(stack_size):
        emit(f"GET YOUR ASS TO MARS s{i}")
        emit(f"DO IT NOW condWrite sp {i} s{i} operand")
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit_end_if()
    emit()

    # ── LOAD ─────────────────────────────────────────────────────────────
    emit_check_opcode('LOAD')
    if num_vars > 0:
        emit("GET YOUR ASS TO MARS a")
        emit(f"DO IT NOW varRead operand {v_args}")
    else:
        emit("GET TO THE CHOPPER a")
        emit("HERE IS MY INVITATION 0")
        emit("ENOUGH TALK")
    emit_stack_push_a()
    emit_end_if()
    emit()

    # ── STORE ────────────────────────────────────────────────────────────
    emit_check_opcode('STORE')
    emit_stack_pop_into("a")
    emit_var_write_a()
    emit_end_if()
    emit()

    # ── DUP ──────────────────────────────────────────────────────────────
    emit_check_opcode('DUP')
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit(f"DO IT NOW stackRead spTmp {s_args}")
    emit_stack_push_a()
    emit_end_if()
    emit()

    # ── POP ──────────────────────────────────────────────────────────────
    emit_check_opcode('POP')
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit_end_if()
    emit()

    # ── INC ──────────────────────────────────────────────────────────────
    emit_check_opcode('INC')
    if num_vars > 0:
        emit("GET YOUR ASS TO MARS a")
        emit(f"DO IT NOW varRead operand {v_args}")
        emit("GET TO THE CHOPPER a")
        emit("HERE IS MY INVITATION a")
        emit("GET UP 1")
        emit("ENOUGH TALK")
        emit_var_write_a()
    emit_end_if()
    emit()

    # ── DEC ──────────────────────────────────────────────────────────────
    emit_check_opcode('DEC')
    if num_vars > 0:
        emit("GET YOUR ASS TO MARS a")
        emit(f"DO IT NOW varRead operand {v_args}")
        emit("GET TO THE CHOPPER a")
        emit("HERE IS MY INVITATION a")
        emit("GET DOWN 1")
        emit("ENOUGH TALK")
        emit_var_write_a()
    emit_end_if()
    emit()

    # ── Binary arithmetic: ADD SUB MUL DIV MOD ──────────────────────────
    binops = [
        ('ADD', 'GET UP'),
        ('SUB', 'GET DOWN'),
        ('MUL', "YOU'RE FIRED"),
        ('DIV', 'HE HAD TO SPLIT'),
        ('MOD', 'I LET HIM GO'),
    ]
    for op_name, kw in binops:
        emit_check_opcode(op_name)
        emit_stack_pop_into("b")          # b = top
        emit_stack_pop_into("a")          # a = second
        emit("GET TO THE CHOPPER result")
        emit("HERE IS MY INVITATION a")
        emit(f"{kw} b")
        emit("ENOUGH TALK")
        # Push result
        emit("GET TO THE CHOPPER a")
        emit("HERE IS MY INVITATION result")
        emit("ENOUGH TALK")
        emit_stack_push_a()
        emit_end_if()
        emit()

    # ── EQ ───────────────────────────────────────────────────────────────
    emit_check_opcode('EQ')
    emit_stack_pop_into("b")
    emit_stack_pop_into("a")
    emit("GET TO THE CHOPPER result")
    emit("HERE IS MY INVITATION a")
    emit("YOU ARE NOT YOU YOU ARE ME b")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER a")
    emit("HERE IS MY INVITATION result")
    emit("ENOUGH TALK")
    emit_stack_push_a()
    emit_end_if()
    emit()

    # ── LT  (second < first  ⇔  first > second  ⇔  b > a) ─────────────
    emit_check_opcode('LT')
    emit_stack_pop_into("b")
    emit_stack_pop_into("a")
    emit("GET TO THE CHOPPER result")
    emit("HERE IS MY INVITATION b")
    emit("LET OFF SOME STEAM BENNET a")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER a")
    emit("HERE IS MY INVITATION result")
    emit("ENOUGH TALK")
    emit_stack_push_a()
    emit_end_if()
    emit()

    # ── GT  (second > first  ⇔  a > b) ─────────────────────────────────
    emit_check_opcode('GT')
    emit_stack_pop_into("b")
    emit_stack_pop_into("a")
    emit("GET TO THE CHOPPER result")
    emit("HERE IS MY INVITATION a")
    emit("LET OFF SOME STEAM BENNET b")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER a")
    emit("HERE IS MY INVITATION result")
    emit("ENOUGH TALK")
    emit_stack_push_a()
    emit_end_if()
    emit()

    # ── AND ──────────────────────────────────────────────────────────────
    emit_check_opcode('AND')
    emit_stack_pop_into("b")
    emit_stack_pop_into("a")
    emit("GET TO THE CHOPPER result")
    emit("HERE IS MY INVITATION a")
    emit("KNOCK KNOCK b")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER a")
    emit("HERE IS MY INVITATION result")
    emit("ENOUGH TALK")
    emit_stack_push_a()
    emit_end_if()
    emit()

    # ── OR ───────────────────────────────────────────────────────────────
    emit_check_opcode('OR')
    emit_stack_pop_into("b")
    emit_stack_pop_into("a")
    emit("GET TO THE CHOPPER result")
    emit("HERE IS MY INVITATION a")
    emit("CONSIDER THAT A DIVORCE b")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER a")
    emit("HERE IS MY INVITATION result")
    emit("ENOUGH TALK")
    emit_stack_push_a()
    emit_end_if()
    emit()

    # ── NOT ──────────────────────────────────────────────────────────────
    emit_check_opcode('NOT')
    # Read top, compute NOT, write back in place
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit(f"DO IT NOW stackRead spTmp {s_args}")
    emit("GET TO THE CHOPPER a")
    emit("HERE IS MY INVITATION a")
    emit("YOU ARE NOT YOU YOU ARE ME 0")    # a = (a == 0)
    emit("ENOUGH TALK")
    emit_stack_write_at("spTmp", "a")
    emit_end_if()
    emit()

    # ── SWAP ─────────────────────────────────────────────────────────────
    emit_check_opcode('SWAP')
    # Read b = stack[sp-1] (top), a = stack[sp-2] (second)
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS b")
    emit(f"DO IT NOW stackRead spTmp {s_args}")
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 2")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit(f"DO IT NOW stackRead spTmp {s_args}")
    # Write b to sp-2
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 2")
    emit("ENOUGH TALK")
    emit_stack_write_at("spTmp", "b")
    # Write a to sp-1
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit_stack_write_at("spTmp", "a")
    emit_end_if()
    emit()

    # ── ROT  [..., a, b, c] → [..., b, c, a] ────────────────────────────
    emit_check_opcode('ROT')
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS c")
    emit(f"DO IT NOW stackRead spTmp {s_args}")
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 2")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS b")
    emit(f"DO IT NOW stackRead spTmp {s_args}")
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 3")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit(f"DO IT NOW stackRead spTmp {s_args}")
    # Write b to sp-3, c to sp-2, a to sp-1
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 3")
    emit("ENOUGH TALK")
    emit_stack_write_at("spTmp", "b")
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 2")
    emit("ENOUGH TALK")
    emit_stack_write_at("spTmp", "c")
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit_stack_write_at("spTmp", "a")
    emit_end_if()
    emit()

    # ── JMP ──────────────────────────────────────────────────────────────
    emit_check_opcode('JMP')
    emit_set_jump()
    emit_end_if()
    emit()

    # ── JZ  (pop; if zero → jump) — uses nested if ──────────────────────
    emit_check_opcode('JZ')
    emit_stack_pop_into("a")
    emit("GET TO THE CHOPPER result")
    emit("HERE IS MY INVITATION a")
    emit("YOU ARE NOT YOU YOU ARE ME 0")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE result")   # nested if
    emit_set_jump()
    emit_end_if()   # end nested
    emit_end_if()   # end JZ
    emit()

    # ── JNZ (pop; if non-zero → jump) — uses nested if/else ─────────────
    emit_check_opcode('JNZ')
    emit_stack_pop_into("a")
    emit("GET TO THE CHOPPER result")
    emit("HERE IS MY INVITATION a")
    emit("YOU ARE NOT YOU YOU ARE ME 0")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE result")   # if a==0
    emit("BULLSHIT")                                   # else (a!=0)
    emit_set_jump()
    emit_end_if()   # end nested
    emit_end_if()   # end JNZ
    emit()

    # ── CALL ─────────────────────────────────────────────────────────────
    emit_check_opcode('CALL')
    # Push ip+1 onto call stack
    emit("GET TO THE CHOPPER a")
    emit("HERE IS MY INVITATION ip")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    for i in range(call_stack_size):
        emit(f"GET YOUR ASS TO MARS cs{i}")
        emit(f"DO IT NOW condWrite csp {i} cs{i} a")
    emit("GET TO THE CHOPPER csp")
    emit("HERE IS MY INVITATION csp")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit_set_jump()
    emit_end_if()
    emit()

    # ── RET ──────────────────────────────────────────────────────────────
    emit_check_opcode('RET')
    emit("GET TO THE CHOPPER csp")
    emit("HERE IS MY INVITATION csp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit(f"DO IT NOW csRead csp {cs_args}")
    emit("GET TO THE CHOPPER ip")
    emit("HERE IS MY INVITATION a")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER jumped")
    emit("HERE IS MY INVITATION 1")
    emit("ENOUGH TALK")
    emit_end_if()
    emit()

    # ── PRINT ────────────────────────────────────────────────────────────
    emit_check_opcode('PRINT')
    emit_stack_pop_into("a")
    emit("TALK TO THE HAND a")
    emit_end_if()
    emit()

    # ── PRINT_STR ────────────────────────────────────────────────────────
    if strings:
        emit_check_opcode('PRINT_STR')
        emit("GET YOUR ASS TO MARS dummy")
        emit("DO IT NOW printStr operand")
        emit_end_if()
        emit()

    # ── EMIT_CHAR (best-effort: prints integer value) ────────────────────
    emit_check_opcode('EMIT_CHAR')
    emit_stack_pop_into("a")
    emit("TALK TO THE HAND a")
    emit_end_if()
    emit()

    # ── READ_INT ─────────────────────────────────────────────────────────
    if int_queues:
        emit_check_opcode('READ_INT')
        if num_queues == 1:
            # Fast path: single queue
            emit("GET YOUR ASS TO MARS a")
            emit("DO IT NOW readIntVal operand iqp0")
            emit_stack_push_a()
            emit("GET TO THE CHOPPER iqp0")
            emit("HERE IS MY INVITATION iqp0")
            emit("GET UP 1")
            emit("ENOUGH TALK")
        else:
            # Multi-queue: use getIqp helper
            iqp_args = " ".join(f"iqp{i}" for i in range(num_queues))
            emit("GET YOUR ASS TO MARS spTmp")
            emit(f"DO IT NOW getIqp operand {iqp_args}")
            emit("GET YOUR ASS TO MARS a")
            emit("DO IT NOW readIntVal operand spTmp")
            emit_stack_push_a()
            # Advance the correct queue pointer
            for qi in range(num_queues):
                emit("GET TO THE CHOPPER b")
                emit(f"HERE IS MY INVITATION iqp{qi}")
                emit("GET UP 1")
                emit("ENOUGH TALK")
                emit(f"GET YOUR ASS TO MARS iqp{qi}")
                emit(f"DO IT NOW condWrite operand {qi} iqp{qi} b")
        emit_end_if()
        emit()

    # ── NEWLINE (no-op: TALK TO THE HAND already appends \n) ────────────
    # Nothing to emit.

    # ── Advance ip if no jump was taken ──────────────────────────────────
    emit("GET TO THE CHOPPER notJumped")
    emit("HERE IS MY INVITATION 1")
    emit("GET DOWN jumped")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE notJumped")
    emit("GET TO THE CHOPPER ip")
    emit("HERE IS MY INVITATION ip")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit_end_if()
    emit()

    # End main loop
    emit("CHILL")
    emit()
    emit("YOU HAVE BEEN TERMINATED")
    emit()

    # ═══════════════════════════════════════════════════════════════════════
    # C.  METHODS
    # ═══════════════════════════════════════════════════════════════════════

    # ── fetchOpcode(idx) ─────────────────────────────────────────────────
    emit("LISTEN TO ME VERY CAREFULLY fetchOpcode")
    emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE idx")
    emit("GIVE THESE PEOPLE AIR")
    emit("HEY CHRISTMAS TREE result")
    emit("YOU SET US UP 0")
    emit("HEY CHRISTMAS TREE eq")
    emit("YOU SET US UP 0")
    for i in range(prog_size):
        emit("GET TO THE CHOPPER eq")
        emit("HERE IS MY INVITATION idx")
        emit(f"YOU ARE NOT YOU YOU ARE ME {i}")
        emit("ENOUGH TALK")
        emit("BECAUSE I'M GOING TO SAY PLEASE eq")
        emit("GET TO THE CHOPPER result")
        emit(f"HERE IS MY INVITATION {enc_op[i]}")
        emit("ENOUGH TALK")
        emit_end_if()
    emit("I'LL BE BACK result")
    emit("HASTA LA VISTA, BABY")
    emit()

    # ── fetchOperand(idx) ────────────────────────────────────────────────
    emit("LISTEN TO ME VERY CAREFULLY fetchOperand")
    emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE idx")
    emit("GIVE THESE PEOPLE AIR")
    emit("HEY CHRISTMAS TREE result")
    emit("YOU SET US UP 0")
    emit("HEY CHRISTMAS TREE eq")
    emit("YOU SET US UP 0")
    for i in range(prog_size):
        emit("GET TO THE CHOPPER eq")
        emit("HERE IS MY INVITATION idx")
        emit(f"YOU ARE NOT YOU YOU ARE ME {i}")
        emit("ENOUGH TALK")
        emit("BECAUSE I'M GOING TO SAY PLEASE eq")
        emit("GET TO THE CHOPPER result")
        emit(f"HERE IS MY INVITATION {enc_arg[i]}")
        emit("ENOUGH TALK")
        emit_end_if()
    emit("I'LL BE BACK result")
    emit("HASTA LA VISTA, BABY")
    emit()

    # ── stackRead(idx, p0 … pN) ─────────────────────────────────────────
    emit("LISTEN TO ME VERY CAREFULLY stackRead")
    emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE idx")
    for i in range(stack_size):
        emit(f"I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE p{i}")
    emit("GIVE THESE PEOPLE AIR")
    emit("HEY CHRISTMAS TREE result")
    emit("YOU SET US UP 0")
    emit("HEY CHRISTMAS TREE eq")
    emit("YOU SET US UP 0")
    for i in range(stack_size):
        emit("GET TO THE CHOPPER eq")
        emit("HERE IS MY INVITATION idx")
        emit(f"YOU ARE NOT YOU YOU ARE ME {i}")
        emit("ENOUGH TALK")
        emit("BECAUSE I'M GOING TO SAY PLEASE eq")
        emit("GET TO THE CHOPPER result")
        emit(f"HERE IS MY INVITATION p{i}")
        emit("ENOUGH TALK")
        emit_end_if()
    emit("I'LL BE BACK result")
    emit("HASTA LA VISTA, BABY")
    emit()

    # ── condWrite(targetIdx, cellIdx, oldVal, newVal) ────────────────────
    emit("LISTEN TO ME VERY CAREFULLY condWrite")
    emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE targetIdx")
    emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE cellIdx")
    emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE oldVal")
    emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE newVal")
    emit("GIVE THESE PEOPLE AIR")
    emit("HEY CHRISTMAS TREE result")
    emit("YOU SET US UP 0")
    emit("HEY CHRISTMAS TREE eq")
    emit("YOU SET US UP 0")
    emit("GET TO THE CHOPPER eq")
    emit("HERE IS MY INVITATION targetIdx")
    emit("YOU ARE NOT YOU YOU ARE ME cellIdx")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE eq")
    emit("GET TO THE CHOPPER result")
    emit("HERE IS MY INVITATION newVal")
    emit("ENOUGH TALK")
    emit("BULLSHIT")
    emit("GET TO THE CHOPPER result")
    emit("HERE IS MY INVITATION oldVal")
    emit("ENOUGH TALK")
    emit_end_if()
    emit("I'LL BE BACK result")
    emit("HASTA LA VISTA, BABY")
    emit()

    # ── varRead(idx, p0 … pK) ───────────────────────────────────────────
    if num_vars > 0:
        emit("LISTEN TO ME VERY CAREFULLY varRead")
        emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE idx")
        for i in range(num_vars):
            emit(f"I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE p{i}")
        emit("GIVE THESE PEOPLE AIR")
        emit("HEY CHRISTMAS TREE result")
        emit("YOU SET US UP 0")
        emit("HEY CHRISTMAS TREE eq")
        emit("YOU SET US UP 0")
        for i in range(num_vars):
            emit("GET TO THE CHOPPER eq")
            emit("HERE IS MY INVITATION idx")
            emit(f"YOU ARE NOT YOU YOU ARE ME {i}")
            emit("ENOUGH TALK")
            emit("BECAUSE I'M GOING TO SAY PLEASE eq")
            emit("GET TO THE CHOPPER result")
            emit(f"HERE IS MY INVITATION p{i}")
            emit("ENOUGH TALK")
            emit_end_if()
        emit("I'LL BE BACK result")
        emit("HASTA LA VISTA, BABY")
        emit()

    # ── csRead(idx, p0 … pM) ────────────────────────────────────────────
    emit("LISTEN TO ME VERY CAREFULLY csRead")
    emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE idx")
    for i in range(call_stack_size):
        emit(f"I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE p{i}")
    emit("GIVE THESE PEOPLE AIR")
    emit("HEY CHRISTMAS TREE result")
    emit("YOU SET US UP 0")
    emit("HEY CHRISTMAS TREE eq")
    emit("YOU SET US UP 0")
    for i in range(call_stack_size):
        emit("GET TO THE CHOPPER eq")
        emit("HERE IS MY INVITATION idx")
        emit(f"YOU ARE NOT YOU YOU ARE ME {i}")
        emit("ENOUGH TALK")
        emit("BECAUSE I'M GOING TO SAY PLEASE eq")
        emit("GET TO THE CHOPPER result")
        emit(f"HERE IS MY INVITATION p{i}")
        emit("ENOUGH TALK")
        emit_end_if()
    emit("I'LL BE BACK result")
    emit("HASTA LA VISTA, BABY")
    emit()

    # ── printStr(idx) ────────────────────────────────────────────────────
    if strings:
        emit("LISTEN TO ME VERY CAREFULLY printStr")
        emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE idx")
        emit("GIVE THESE PEOPLE AIR")
        emit("HEY CHRISTMAS TREE eq")
        emit("YOU SET US UP 0")
        for i, s in enumerate(strings):
            emit("GET TO THE CHOPPER eq")
            emit("HERE IS MY INVITATION idx")
            emit(f"YOU ARE NOT YOU YOU ARE ME {i}")
            emit("ENOUGH TALK")
            emit("BECAUSE I'M GOING TO SAY PLEASE eq")
            escaped = s.replace('\\', '\\\\').replace('"', '\\"')
            emit(f'TALK TO THE HAND "{escaped}"')
            emit_end_if()
        emit("I'LL BE BACK 0")
        emit("HASTA LA VISTA, BABY")
        emit()

    # ── readIntVal(queueId, pos) ─────────────────────────────────────────
    if int_queues:
        emit("LISTEN TO ME VERY CAREFULLY readIntVal")
        emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE queueId")
        emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE pos")
        emit("GIVE THESE PEOPLE AIR")
        emit("HEY CHRISTMAS TREE result")
        emit("YOU SET US UP 0")
        emit("HEY CHRISTMAS TREE eq1")
        emit("YOU SET US UP 0")
        emit("HEY CHRISTMAS TREE eq2")
        emit("YOU SET US UP 0")
        emit("HEY CHRISTMAS TREE match")
        emit("YOU SET US UP 0")
        for qi, queue in enumerate(int_queues):
            for pi, val in enumerate(queue):
                emit("GET TO THE CHOPPER eq1")
                emit("HERE IS MY INVITATION queueId")
                emit(f"YOU ARE NOT YOU YOU ARE ME {qi}")
                emit("ENOUGH TALK")
                emit("GET TO THE CHOPPER eq2")
                emit("HERE IS MY INVITATION pos")
                emit(f"YOU ARE NOT YOU YOU ARE ME {pi}")
                emit("ENOUGH TALK")
                emit("GET TO THE CHOPPER match")
                emit("HERE IS MY INVITATION eq1")
                emit("KNOCK KNOCK eq2")
                emit("ENOUGH TALK")
                emit("BECAUSE I'M GOING TO SAY PLEASE match")
                emit("GET TO THE CHOPPER result")
                emit(f"HERE IS MY INVITATION {val}")
                emit("ENOUGH TALK")
                emit_end_if()
        emit("I'LL BE BACK result")
        emit("HASTA LA VISTA, BABY")
        emit()

    # ── getIqp(queueId, p0 … pQ) — only for multi-queue programs ────────
    if num_queues > 1:
        emit("LISTEN TO ME VERY CAREFULLY getIqp")
        emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE queueId")
        for qi in range(num_queues):
            emit(f"I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE p{qi}")
        emit("GIVE THESE PEOPLE AIR")
        emit("HEY CHRISTMAS TREE result")
        emit("YOU SET US UP 0")
        emit("HEY CHRISTMAS TREE eq")
        emit("YOU SET US UP 0")
        for qi in range(num_queues):
            emit("GET TO THE CHOPPER eq")
            emit("HERE IS MY INVITATION queueId")
            emit(f"YOU ARE NOT YOU YOU ARE ME {qi}")
            emit("ENOUGH TALK")
            emit("BECAUSE I'M GOING TO SAY PLEASE eq")
            emit("GET TO THE CHOPPER result")
            emit(f"HERE IS MY INVITATION p{qi}")
            emit("ENOUGH TALK")
            emit_end_if()
        emit("I'LL BE BACK result")
        emit("HASTA LA VISTA, BABY")
        emit()

    source = "\n".join(lines) + "\n"
    if output_path:
        with open(output_path, 'w') as f:
            f.write(source)
    return source


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 generate_mnm_interpreter.py PROG.mnm PROG.mnm.json [OUTPUT.arnoldc]")
        sys.exit(1)

    mnm_path = sys.argv[1]
    json_path = sys.argv[2]
    out_path = sys.argv[3] if len(sys.argv) > 3 else mnm_path.replace('.mnm', '_mnm.arnoldc')

    with open(mnm_path) as f:
        mnm_source = f.read()
    with open(json_path) as f:
        sidecar = json.load(f)

    source = generate(mnm_source, sidecar, output_path=out_path)
    n_lines = source.count('\n')
    print(f"Generated {n_lines} lines → {out_path}")

    # Show parsed instructions for debugging
    raw = parse_mnm(mnm_source)
    resolved, labels = resolve_labels(raw)
    print(f"  {len(resolved)} instructions, {len(labels)} labels")
    for i, (op, arg) in enumerate(resolved):
        print(f"  [{i:3d}] {op:12s}  {arg}")
