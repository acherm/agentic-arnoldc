#!/usr/bin/env python3
"""Build a fixed MnM Lang interpreter in ArnoldC.

Unlike generate_mnm_interpreter.py (which produces different ArnoldC per input),
this generates a SINGLE FIXED ArnoldC program that reads any MnM program from
stdin and executes it — a true interpreter, architecturally matching brainfuck.arnoldc.

The output is always the same file regardless of input. The Python script is just
a convenience to avoid hand-typing ~7000 lines of repetitive ArnoldC.

Requires the patched ArnoldC compiler (static fields support).

Fixed limits:
  PROG_SIZE  = 100  (max MnM instructions)
  STACK_SIZE = 30   (max stack depth)
  VAR_SIZE   = 50   (max MnM variables)
  CS_SIZE    = 10   (max call nesting)
  IQ_SIZE    = 10   (max input queue values)

Input protocol (integers from stdin):
  1. progLen                       (number of instructions)
  2. progLen × (opcode, operand)   (instruction pairs)
  3. numVars                       (number of variable initial values)
  4. numVars × value               (initial values)
  5. numInputs                     (number of input queue values)
  6. numInputs × value             (input values)

Usage:
  python3 build_mnm_vm.py                    # generates mnm_vm.arnoldc
  java -jar ArnoldC-patched.jar mnm_vm.arnoldc   # compile once
  echo "3 10 1 40 0 0 0 45 0 0 0 0 0" | java mnm_vm  # run: PUSH 1, PRINT, HALT → prints 1
"""

import os
import sys

# ── Fixed sizes ──────────────────────────────────────────────────────────────

PROG_SIZE  = 100   # instruction slots
STACK_SIZE = 30    # stack cells
VAR_SIZE   = 50    # MnM variable slots
CS_SIZE    = 10    # call stack levels
IQ_SIZE    = 10    # input queue values

# ── Internal opcode numbers (same as generate_mnm_interpreter.py) ────────────

OPCODES = {
    'HALT': 0,   'NOP': 1,
    'PUSH': 10,  'LOAD': 11,  'STORE': 12,  'DUP': 13,
    'POP': 14,   'INC': 15,   'DEC': 16,
    'ADD': 20,   'SUB': 21,   'MUL': 22,    'DIV': 23,   'MOD': 24,
    'EQ': 25,    'LT': 26,    'GT': 27,
    'JMP': 30,   'JZ': 31,    'JNZ': 32,    'CALL': 33,  'RET': 34,
    'PRINT': 40, 'READ_INT': 42, 'EMIT_CHAR': 44, 'NEWLINE': 45,
    'SWAP': 50,  'ROT': 51,   'AND': 52,    'OR': 53,    'NOT': 54,
}


def build():
    lines = []

    def emit(s=""):
        lines.append(s)

    def emit_end_if():
        emit("YOU HAVE NO RESPECT FOR LOGIC")

    # ═════════════════════════════════════════════════════════════════════
    # A.  VARIABLE DECLARATIONS (all become static fields)
    # ═════════════════════════════════════════════════════════════════════
    emit("IT'S SHOWTIME")
    emit()

    # Program storage
    for i in range(PROG_SIZE):
        emit(f"HEY CHRISTMAS TREE po{i}")
        emit("YOU SET US UP 0")
    for i in range(PROG_SIZE):
        emit(f"HEY CHRISTMAS TREE pa{i}")
        emit("YOU SET US UP 0")
    emit()

    # Stack
    for i in range(STACK_SIZE):
        emit(f"HEY CHRISTMAS TREE s{i}")
        emit("YOU SET US UP 0")
    emit()

    # Variables
    for i in range(VAR_SIZE):
        emit(f"HEY CHRISTMAS TREE v{i}")
        emit("YOU SET US UP 0")
    emit()

    # Call stack
    for i in range(CS_SIZE):
        emit(f"HEY CHRISTMAS TREE cs{i}")
        emit("YOU SET US UP 0")
    emit()

    # Input queue
    for i in range(IQ_SIZE):
        emit(f"HEY CHRISTMAS TREE iq{i}")
        emit("YOU SET US UP 0")
    emit()

    # Control variables
    ctrl = [
        ("ip", 0), ("sp", 0), ("csp", 0), ("iqp", 0),
        ("running", 1), ("opcode", 0), ("operand", 0),
        ("a", 0), ("b", 0), ("c", 0), ("result", 0),
        ("isOp", 0), ("jumped", 0), ("notJumped", 0), ("spTmp", 0),
        ("progLen", 0), ("numVars", 0), ("numInputs", 0),
        ("readIdx", 0), ("readCond", 0),
    ]
    for name, val in ctrl:
        emit(f"HEY CHRISTMAS TREE {name}")
        emit(f"YOU SET US UP {val}")
    emit()

    # ═════════════════════════════════════════════════════════════════════
    # B.  READ PROGRAM FROM STDIN
    # ═════════════════════════════════════════════════════════════════════

    def emit_read_into(var):
        """Read one integer from stdin into var."""
        emit(f"GET YOUR ASS TO MARS {var}")
        emit("DO IT NOW")
        emit("I WANT TO ASK YOU A BUNCH OF QUESTIONS AND I WANT TO HAVE THEM ANSWERED IMMEDIATELY")

    def emit_read_loop(count_var, write_method, read_per_iter=1):
        """Emit a loop that reads count_var items from stdin via write_method."""
        emit("GET TO THE CHOPPER readIdx")
        emit("HERE IS MY INVITATION 0")
        emit("ENOUGH TALK")
        emit(f"GET TO THE CHOPPER readCond")
        emit(f"HERE IS MY INVITATION {count_var}")
        emit("LET OFF SOME STEAM BENNET readIdx")
        emit("ENOUGH TALK")
        emit("STICK AROUND readCond")
        if read_per_iter == 2:
            # Read opcode + operand pair
            emit_read_into("a")
            emit(f"DO IT NOW {write_method}Op readIdx a")
            emit_read_into("a")
            emit(f"DO IT NOW {write_method}Arg readIdx a")
        else:
            emit_read_into("a")
            emit(f"DO IT NOW {write_method} readIdx a")
        emit("GET TO THE CHOPPER readIdx")
        emit("HERE IS MY INVITATION readIdx")
        emit("GET UP 1")
        emit("ENOUGH TALK")
        emit(f"GET TO THE CHOPPER readCond")
        emit(f"HERE IS MY INVITATION {count_var}")
        emit("LET OFF SOME STEAM BENNET readIdx")
        emit("ENOUGH TALK")
        emit("CHILL")
        emit()

    # Read progLen, then progLen instruction pairs
    emit_read_into("progLen")
    emit_read_loop("progLen", "progWrite", read_per_iter=2)

    # Read numVars, then initial values
    emit_read_into("numVars")
    emit_read_loop("numVars", "varInit")

    # Read numInputs, then input queue values
    emit_read_into("numInputs")
    emit_read_loop("numInputs", "iqInit")

    # ═════════════════════════════════════════════════════════════════════
    # C.  MAIN EXECUTION LOOP
    # ═════════════════════════════════════════════════════════════════════
    emit("STICK AROUND running")
    emit()

    # Fetch
    emit("GET YOUR ASS TO MARS opcode")
    emit("DO IT NOW fetchOp ip")
    emit("GET YOUR ASS TO MARS operand")
    emit("DO IT NOW fetchArg ip")
    emit()

    # Reset jumped
    emit("GET TO THE CHOPPER jumped")
    emit("HERE IS MY INVITATION 0")
    emit("ENOUGH TALK")
    emit()

    def check_op(name):
        emit("GET TO THE CHOPPER isOp")
        emit("HERE IS MY INVITATION opcode")
        emit(f"YOU ARE NOT YOU YOU ARE ME {OPCODES[name]}")
        emit("ENOUGH TALK")
        emit("BECAUSE I'M GOING TO SAY PLEASE isOp")

    def end_op():
        emit_end_if()
        emit()

    # ── HALT ────────────────────────────────────────────────────────
    check_op('HALT')
    emit("GET TO THE CHOPPER running")
    emit("HERE IS MY INVITATION 0")
    emit("ENOUGH TALK")
    end_op()

    # ── PUSH ────────────────────────────────────────────────────────
    check_op('PUSH')
    emit("DO IT NOW stackW sp operand")
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    end_op()

    # ── LOAD ────────────────────────────────────────────────────────
    check_op('LOAD')
    emit("GET YOUR ASS TO MARS a")
    emit("DO IT NOW varR operand")
    emit("DO IT NOW stackW sp a")
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    end_op()

    # ── STORE ───────────────────────────────────────────────────────
    check_op('STORE')
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit("DO IT NOW stackR sp")
    emit("DO IT NOW varW operand a")
    end_op()

    # ── DUP ─────────────────────────────────────────────────────────
    check_op('DUP')
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit("DO IT NOW stackR spTmp")
    emit("DO IT NOW stackW sp a")
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    end_op()

    # ── POP ─────────────────────────────────────────────────────────
    check_op('POP')
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    end_op()

    # ── INC ─────────────────────────────────────────────────────────
    check_op('INC')
    emit("GET YOUR ASS TO MARS a")
    emit("DO IT NOW varR operand")
    emit("GET TO THE CHOPPER a")
    emit("HERE IS MY INVITATION a")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit("DO IT NOW varW operand a")
    end_op()

    # ── DEC ─────────────────────────────────────────────────────────
    check_op('DEC')
    emit("GET YOUR ASS TO MARS a")
    emit("DO IT NOW varR operand")
    emit("GET TO THE CHOPPER a")
    emit("HERE IS MY INVITATION a")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("DO IT NOW varW operand a")
    end_op()

    # ── Binary arithmetic ───────────────────────────────────────────
    binops = [
        ('ADD', 'GET UP'),
        ('SUB', 'GET DOWN'),
        ('MUL', "YOU'RE FIRED"),
        ('DIV', 'HE HAD TO SPLIT'),
        ('MOD', 'I LET HIM GO'),
    ]
    for op_name, kw in binops:
        check_op(op_name)
        # Pop b (top)
        emit("GET TO THE CHOPPER sp")
        emit("HERE IS MY INVITATION sp")
        emit("GET DOWN 1")
        emit("ENOUGH TALK")
        emit("GET YOUR ASS TO MARS b")
        emit("DO IT NOW stackR sp")
        # Pop a (second)
        emit("GET TO THE CHOPPER sp")
        emit("HERE IS MY INVITATION sp")
        emit("GET DOWN 1")
        emit("ENOUGH TALK")
        emit("GET YOUR ASS TO MARS a")
        emit("DO IT NOW stackR sp")
        # result = a OP b
        emit("GET TO THE CHOPPER result")
        emit("HERE IS MY INVITATION a")
        emit(f"{kw} b")
        emit("ENOUGH TALK")
        # Push result
        emit("DO IT NOW stackW sp result")
        emit("GET TO THE CHOPPER sp")
        emit("HERE IS MY INVITATION sp")
        emit("GET UP 1")
        emit("ENOUGH TALK")
        end_op()

    # ── EQ ──────────────────────────────────────────────────────────
    check_op('EQ')
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS b")
    emit("DO IT NOW stackR sp")
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit("DO IT NOW stackR sp")
    emit("GET TO THE CHOPPER result")
    emit("HERE IS MY INVITATION a")
    emit("YOU ARE NOT YOU YOU ARE ME b")
    emit("ENOUGH TALK")
    emit("DO IT NOW stackW sp result")
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    end_op()

    # ── LT (second < first ⇔ b > a) ───────────────────────────────
    check_op('LT')
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS b")
    emit("DO IT NOW stackR sp")
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit("DO IT NOW stackR sp")
    emit("GET TO THE CHOPPER result")
    emit("HERE IS MY INVITATION b")
    emit("LET OFF SOME STEAM BENNET a")
    emit("ENOUGH TALK")
    emit("DO IT NOW stackW sp result")
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    end_op()

    # ── GT (second > first ⇔ a > b) ───────────────────────────────
    check_op('GT')
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS b")
    emit("DO IT NOW stackR sp")
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit("DO IT NOW stackR sp")
    emit("GET TO THE CHOPPER result")
    emit("HERE IS MY INVITATION a")
    emit("LET OFF SOME STEAM BENNET b")
    emit("ENOUGH TALK")
    emit("DO IT NOW stackW sp result")
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    end_op()

    # ── AND ─────────────────────────────────────────────────────────
    check_op('AND')
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS b")
    emit("DO IT NOW stackR sp")
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit("DO IT NOW stackR sp")
    emit("GET TO THE CHOPPER result")
    emit("HERE IS MY INVITATION a")
    emit("KNOCK KNOCK b")
    emit("ENOUGH TALK")
    emit("DO IT NOW stackW sp result")
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    end_op()

    # ── OR ──────────────────────────────────────────────────────────
    check_op('OR')
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS b")
    emit("DO IT NOW stackR sp")
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit("DO IT NOW stackR sp")
    emit("GET TO THE CHOPPER result")
    emit("HERE IS MY INVITATION a")
    emit("CONSIDER THAT A DIVORCE b")
    emit("ENOUGH TALK")
    emit("DO IT NOW stackW sp result")
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    end_op()

    # ── NOT ─────────────────────────────────────────────────────────
    check_op('NOT')
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit("DO IT NOW stackR spTmp")
    emit("GET TO THE CHOPPER a")
    emit("HERE IS MY INVITATION a")
    emit("YOU ARE NOT YOU YOU ARE ME 0")
    emit("ENOUGH TALK")
    emit("DO IT NOW stackW spTmp a")
    end_op()

    # ── SWAP ────────────────────────────────────────────────────────
    check_op('SWAP')
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS b")
    emit("DO IT NOW stackR spTmp")
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 2")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit("DO IT NOW stackR spTmp")
    # Write b to sp-2, a to sp-1
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 2")
    emit("ENOUGH TALK")
    emit("DO IT NOW stackW spTmp b")
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("DO IT NOW stackW spTmp a")
    end_op()

    # ── ROT  [..., a, b, c] → [..., b, c, a] ──────────────────────
    check_op('ROT')
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS c")
    emit("DO IT NOW stackR spTmp")
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 2")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS b")
    emit("DO IT NOW stackR spTmp")
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 3")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit("DO IT NOW stackR spTmp")
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 3")
    emit("ENOUGH TALK")
    emit("DO IT NOW stackW spTmp b")
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 2")
    emit("ENOUGH TALK")
    emit("DO IT NOW stackW spTmp c")
    emit("GET TO THE CHOPPER spTmp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("DO IT NOW stackW spTmp a")
    end_op()

    # ── JMP ─────────────────────────────────────────────────────────
    check_op('JMP')
    emit("GET TO THE CHOPPER ip")
    emit("HERE IS MY INVITATION operand")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER jumped")
    emit("HERE IS MY INVITATION 1")
    emit("ENOUGH TALK")
    end_op()

    # ── JZ (nested if) ──────────────────────────────────────────────
    check_op('JZ')
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit("DO IT NOW stackR sp")
    emit("GET TO THE CHOPPER result")
    emit("HERE IS MY INVITATION a")
    emit("YOU ARE NOT YOU YOU ARE ME 0")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE result")
    emit("GET TO THE CHOPPER ip")
    emit("HERE IS MY INVITATION operand")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER jumped")
    emit("HERE IS MY INVITATION 1")
    emit("ENOUGH TALK")
    emit_end_if()
    end_op()

    # ── JNZ (nested if/else) ────────────────────────────────────────
    check_op('JNZ')
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit("DO IT NOW stackR sp")
    emit("GET TO THE CHOPPER result")
    emit("HERE IS MY INVITATION a")
    emit("YOU ARE NOT YOU YOU ARE ME 0")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE result")
    emit("BULLSHIT")
    emit("GET TO THE CHOPPER ip")
    emit("HERE IS MY INVITATION operand")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER jumped")
    emit("HERE IS MY INVITATION 1")
    emit("ENOUGH TALK")
    emit_end_if()
    end_op()

    # ── CALL ────────────────────────────────────────────────────────
    check_op('CALL')
    emit("GET TO THE CHOPPER a")
    emit("HERE IS MY INVITATION ip")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit("DO IT NOW csW csp a")
    emit("GET TO THE CHOPPER csp")
    emit("HERE IS MY INVITATION csp")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER ip")
    emit("HERE IS MY INVITATION operand")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER jumped")
    emit("HERE IS MY INVITATION 1")
    emit("ENOUGH TALK")
    end_op()

    # ── RET ─────────────────────────────────────────────────────────
    check_op('RET')
    emit("GET TO THE CHOPPER csp")
    emit("HERE IS MY INVITATION csp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit("DO IT NOW csR csp")
    emit("GET TO THE CHOPPER ip")
    emit("HERE IS MY INVITATION a")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER jumped")
    emit("HERE IS MY INVITATION 1")
    emit("ENOUGH TALK")
    end_op()

    # ── PRINT ───────────────────────────────────────────────────────
    check_op('PRINT')
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit("DO IT NOW stackR sp")
    emit("TALK TO THE HAND a")
    end_op()

    # ── EMIT_CHAR (prints integer value — ArnoldC limitation) ──────
    check_op('EMIT_CHAR')
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS a")
    emit("DO IT NOW stackR sp")
    emit("TALK TO THE HAND a")
    end_op()

    # ── READ_INT ────────────────────────────────────────────────────
    check_op('READ_INT')
    emit("GET YOUR ASS TO MARS a")
    emit("DO IT NOW iqR iqp")
    emit("GET TO THE CHOPPER iqp")
    emit("HERE IS MY INVITATION iqp")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit("DO IT NOW stackW sp a")
    emit("GET TO THE CHOPPER sp")
    emit("HERE IS MY INVITATION sp")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    end_op()

    # ── Advance ip if no jump ───────────────────────────────────────
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

    emit("CHILL")
    emit()
    emit("YOU HAVE BEEN TERMINATED")
    emit()

    # ═════════════════════════════════════════════════════════════════════
    # D.  METHODS (all access static fields via GETSTATIC/PUTSTATIC)
    # ═════════════════════════════════════════════════════════════════════

    def emit_read_method(name, prefix, size):
        """Non-void method: name(idx) → prefix[idx]."""
        emit(f"LISTEN TO ME VERY CAREFULLY {name}")
        emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE idx")
        emit("GIVE THESE PEOPLE AIR")
        emit("HEY CHRISTMAS TREE res")
        emit("YOU SET US UP 0")
        emit("HEY CHRISTMAS TREE eq")
        emit("YOU SET US UP 0")
        for i in range(size):
            emit("GET TO THE CHOPPER eq")
            emit("HERE IS MY INVITATION idx")
            emit(f"YOU ARE NOT YOU YOU ARE ME {i}")
            emit("ENOUGH TALK")
            emit("BECAUSE I'M GOING TO SAY PLEASE eq")
            emit("GET TO THE CHOPPER res")
            emit(f"HERE IS MY INVITATION {prefix}{i}")
            emit("ENOUGH TALK")
            emit_end_if()
        emit("I'LL BE BACK res")
        emit("HASTA LA VISTA, BABY")
        emit()

    def emit_write_method(name, prefix, size):
        """Void method: name(idx, val) — writes val to prefix[idx]."""
        emit(f"LISTEN TO ME VERY CAREFULLY {name}")
        emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE idx")
        emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE val")
        emit("HEY CHRISTMAS TREE eq")
        emit("YOU SET US UP 0")
        for i in range(size):
            emit("GET TO THE CHOPPER eq")
            emit("HERE IS MY INVITATION idx")
            emit(f"YOU ARE NOT YOU YOU ARE ME {i}")
            emit("ENOUGH TALK")
            emit("BECAUSE I'M GOING TO SAY PLEASE eq")
            emit(f"GET TO THE CHOPPER {prefix}{i}")
            emit("HERE IS MY INVITATION val")
            emit("ENOUGH TALK")
            emit_end_if()
        emit("HASTA LA VISTA, BABY")
        emit()

    # Program read
    emit_read_method("fetchOp", "po", PROG_SIZE)
    emit_read_method("fetchArg", "pa", PROG_SIZE)

    # Program write (used during input phase)
    emit_write_method("progWriteOp", "po", PROG_SIZE)
    emit_write_method("progWriteArg", "pa", PROG_SIZE)

    # Stack
    emit_read_method("stackR", "s", STACK_SIZE)
    emit_write_method("stackW", "s", STACK_SIZE)

    # Variables
    emit_read_method("varR", "v", VAR_SIZE)
    emit_write_method("varW", "v", VAR_SIZE)
    emit_write_method("varInit", "v", VAR_SIZE)  # alias for input phase

    # Call stack
    emit_read_method("csR", "cs", CS_SIZE)
    emit_write_method("csW", "cs", CS_SIZE)

    # Input queue
    emit_read_method("iqR", "iq", IQ_SIZE)
    emit_write_method("iqInit", "iq", IQ_SIZE)

    return "\n".join(lines) + "\n"


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "mnm_vm.arnoldc"
    source = build()
    with open(out_path, "w") as f:
        f.write(source)
    n_lines = source.count('\n')
    print(f"Built {n_lines} lines → {out_path}")
    print(f"  PROG_SIZE={PROG_SIZE}, STACK_SIZE={STACK_SIZE}, VAR_SIZE={VAR_SIZE}, CS_SIZE={CS_SIZE}, IQ_SIZE={IQ_SIZE}")
