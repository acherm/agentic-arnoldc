#!/usr/bin/env python3
"""Generate a minimal MnM Lang Brainfuck interpreter for a given BF program.

The generated MnM program + sidecar can then be fed into
generate_mnm_interpreter.py to produce an ArnoldC program,
achieving: ArnoldC → interprets MnM → interprets Brainfuck.

Variable layout (all within ArnoldC's 100-local limit):
  var 0:  ip  (BF instruction pointer)
  var 1:  dp  (BF data pointer)
  var 2:  prog_len
  var 3:  depth (bracket-matching scratch)
  var 4:  cur_inst (fetched instruction)
  var 5:  cur_val (tape cell value)
  var P..P+N-1:  program (N = len(bf_encoded))
  var T..T+M-1:  tape (M cells)

Usage:
    python3 generate_mnm_bf.py '+++[>++<-]>.'
    python3 generate_mnm_bf.py '+++[>++<-]>.' --run
"""

import json
import os
import subprocess
import sys

BF_ENCODING = {'>': 1, '<': 2, '+': 3, '-': 4, '.': 5, ',': 6, '[': 7, ']': 8}


def mnm_token(color, value):
    """Build a MnM token: repeated color letter, value = len - 1."""
    return color * (value + 1)


def estimate_tape_size(bf_source):
    """Estimate tape cells needed."""
    pos = 0
    mx = 0
    for c in bf_source:
        if c == '>': pos += 1; mx = max(mx, pos)
        elif c == '<': pos -= 1
    return max(mx + 2, 4)


def generate_mnm_bf(bf_source, tape_size=None):
    """Generate MnM source + sidecar for a BF interpreter.

    Returns (mnm_source, sidecar_dict, info_dict).
    """
    bf_encoded = [BF_ENCODING[c] for c in bf_source if c in BF_ENCODING]
    prog_len = len(bf_encoded)
    if tape_size is None:
        tape_size = estimate_tape_size(bf_source)

    PROG_BASE = 6       # program starts at var 6
    TAPE_BASE = PROG_BASE + max(prog_len, 1)
    num_vars = TAPE_BASE + tape_size

    # Sidecar variables
    variables = [0] * num_vars
    variables[2] = prog_len
    for i, code in enumerate(bf_encoded):
        variables[PROG_BASE + i] = code

    lines = []
    label_counter = [0]

    def fresh_label():
        label_counter[0] += 1
        return label_counter[0]

    def emit(line):
        lines.append(line)

    def emit_label(lid):
        emit(f"N {mnm_token('B', lid)}")

    def emit_jmp(lid):
        emit(f"B {mnm_token('B', lid)}")

    def emit_jz(lid):
        emit(f"BB {mnm_token('B', lid)}")

    def emit_jnz(lid):
        emit(f"BBB {mnm_token('B', lid)}")

    def emit_call(lid):
        emit(f"BBBB {mnm_token('B', lid)}")

    def emit_push(val):
        emit(f"G {mnm_token('R', val)}")

    def emit_load(var_idx):
        emit(f"GG {mnm_token('G', var_idx)}")

    def emit_store(var_idx):
        emit(f"GGG {mnm_token('G', var_idx)}")

    def emit_inc(var_idx):
        emit(f"GGGGGG {mnm_token('G', var_idx)}")

    def emit_dec(var_idx):
        emit(f"GGGGGGG {mnm_token('G', var_idx)}")

    def emit_dup():
        emit("GGGG")

    def emit_pop():
        emit("GGGGG")

    def emit_add():
        emit("Y")

    def emit_sub():
        emit("YY")

    def emit_eq():
        emit("YYYYYY")

    def emit_lt():
        emit("YYYYYYY")

    def emit_gt():
        emit("YYYYYYYY")

    def emit_print():
        emit("O")

    def emit_newline():
        emit("OOOOOO")

    def emit_halt():
        emit("BBBBBB")

    def emit_ret():
        emit("BBBBB")

    def emit_swap():
        emit("R")

    # ── Helper: emit a "read array" comparison chain ─────────────────
    # Reads var[base + index_on_stack] by comparing index against 0..size-1
    # Result is pushed onto stack (index is consumed).
    def emit_read_array(base, size, result_var):
        """Read array[TOS] into result_var. Consumes TOS."""
        # Store default 0
        emit_push(0)
        emit_store(result_var)
        for i in range(size):
            lbl_skip = fresh_label()
            emit_dup()                     # dup index
            emit_push(i)                   # push i
            emit_eq()                      # index == i?
            emit_jz(lbl_skip)             # skip if not equal
            emit_load(base + i)           # load var[base+i]
            emit_store(result_var)        # store to result
            emit_label(lbl_skip)
        emit_pop()   # discard index

    # ── Helper: emit a "write array" comparison chain ────────────────
    # Writes value_var into var[base + index_on_stack].
    def emit_write_array(base, size, value_var):
        """Write value_var into array[TOS]. Consumes TOS."""
        for i in range(size):
            lbl_skip = fresh_label()
            emit_dup()
            emit_push(i)
            emit_eq()
            emit_jz(lbl_skip)
            emit_load(value_var)
            emit_store(base + i)
            emit_label(lbl_skip)
        emit_pop()

    # ════════════════════════════════════════════════════════════════════
    # MAIN PROGRAM
    # ════════════════════════════════════════════════════════════════════

    LBL_LOOP = fresh_label()       # main loop
    LBL_EXIT = fresh_label()       # exit
    LBL_NEXT = fresh_label()       # advance ip & loop back
    LBL_PLUS = fresh_label()       # handler: +
    LBL_MINUS = fresh_label()      # handler: -
    LBL_RIGHT = fresh_label()      # handler: >
    LBL_LEFT = fresh_label()       # handler: <
    LBL_DOT = fresh_label()        # handler: .
    LBL_OPEN = fresh_label()       # handler: [
    LBL_CLOSE = fresh_label()      # handler: ]
    LBL_SKIP_INST = fresh_label()  # skip unknown instruction

    # ── Main loop ────────────────────────────────────────────────────
    emit_label(LBL_LOOP)

    # if ip >= prog_len: exit
    emit_load(0)         # ip
    emit_load(2)         # prog_len
    emit_lt()            # ip < prog_len?
    emit_jz(LBL_EXIT)   # if not, exit

    # Fetch program[ip] into var 4
    emit_load(0)         # push ip
    emit_read_array(PROG_BASE, prog_len, 4)

    # Check end marker
    emit_load(4)
    emit_push(0)
    emit_eq()
    emit_jnz(LBL_EXIT)

    # ── Dispatch ─────────────────────────────────────────────────────

    # + (inst == 3)
    emit_load(4); emit_push(3); emit_eq(); emit_jz(LBL_PLUS)
    # Read tape[dp]
    emit_load(1)
    emit_read_array(TAPE_BASE, tape_size, 5)
    emit_inc(5)   # cur_val++
    # Write tape[dp]
    emit_load(1)
    emit_write_array(TAPE_BASE, tape_size, 5)
    emit_jmp(LBL_NEXT)

    # - (inst == 4)
    emit_label(LBL_PLUS)
    emit_load(4); emit_push(4); emit_eq(); emit_jz(LBL_MINUS)
    emit_load(1)
    emit_read_array(TAPE_BASE, tape_size, 5)
    emit_dec(5)
    emit_load(1)
    emit_write_array(TAPE_BASE, tape_size, 5)
    emit_jmp(LBL_NEXT)

    # > (inst == 1)
    emit_label(LBL_MINUS)
    emit_load(4); emit_push(1); emit_eq(); emit_jz(LBL_RIGHT)
    emit_inc(1)
    emit_jmp(LBL_NEXT)

    # < (inst == 2)
    emit_label(LBL_RIGHT)
    emit_load(4); emit_push(2); emit_eq(); emit_jz(LBL_LEFT)
    emit_dec(1)
    emit_jmp(LBL_NEXT)

    # . (inst == 5)
    emit_label(LBL_LEFT)
    emit_load(4); emit_push(5); emit_eq(); emit_jz(LBL_DOT)
    emit_load(1)
    emit_read_array(TAPE_BASE, tape_size, 5)
    emit_load(5)
    emit_print()
    emit_jmp(LBL_NEXT)

    # [ (inst == 7)
    emit_label(LBL_DOT)
    emit_load(4); emit_push(7); emit_eq(); emit_jz(LBL_OPEN)
    # Read tape[dp]
    emit_load(1)
    emit_read_array(TAPE_BASE, tape_size, 5)
    # If cur_val != 0, just advance ip
    emit_load(5)
    emit_push(0)
    emit_eq()
    emit_jz(LBL_NEXT)   # non-zero → continue normally
    # cur_val == 0: scan forward for matching ]
    emit_push(1)
    emit_store(3)   # depth = 1
    LBL_FWD_LOOP = fresh_label()
    LBL_FWD_DONE = fresh_label()
    LBL_FWD_NOT_OPEN = fresh_label()
    LBL_FWD_NOT_CLOSE = fresh_label()
    emit_label(LBL_FWD_LOOP)
    emit_inc(0)   # ip++
    # Fetch program[ip]
    emit_load(0)
    emit_read_array(PROG_BASE, prog_len, 4)
    # if inst == 7, depth++
    emit_load(4); emit_push(7); emit_eq(); emit_jz(LBL_FWD_NOT_OPEN)
    emit_inc(3)
    emit_label(LBL_FWD_NOT_OPEN)
    # if inst == 8, depth--
    emit_load(4); emit_push(8); emit_eq(); emit_jz(LBL_FWD_NOT_CLOSE)
    emit_dec(3)
    emit_label(LBL_FWD_NOT_CLOSE)
    # if depth > 0, continue
    emit_load(3); emit_push(0); emit_gt(); emit_jnz(LBL_FWD_LOOP)
    emit_jmp(LBL_NEXT)

    # ] (inst == 8)
    emit_label(LBL_OPEN)
    emit_load(4); emit_push(8); emit_eq(); emit_jz(LBL_CLOSE)
    # Read tape[dp]
    emit_load(1)
    emit_read_array(TAPE_BASE, tape_size, 5)
    # If cur_val == 0, just advance ip
    emit_load(5)
    emit_push(0)
    emit_eq()
    emit_jnz(LBL_NEXT)   # zero → continue normally
    # cur_val != 0: scan backward for matching [
    emit_push(1)
    emit_store(3)   # depth = 1
    LBL_BWD_LOOP = fresh_label()
    LBL_BWD_NOT_CLOSE = fresh_label()
    LBL_BWD_NOT_OPEN = fresh_label()
    emit_label(LBL_BWD_LOOP)
    emit_dec(0)   # ip--
    emit_load(0)
    emit_read_array(PROG_BASE, prog_len, 4)
    # if inst == 8, depth++
    emit_load(4); emit_push(8); emit_eq(); emit_jz(LBL_BWD_NOT_CLOSE)
    emit_inc(3)
    emit_label(LBL_BWD_NOT_CLOSE)
    # if inst == 7, depth--
    emit_load(4); emit_push(7); emit_eq(); emit_jz(LBL_BWD_NOT_OPEN)
    emit_dec(3)
    emit_label(LBL_BWD_NOT_OPEN)
    # if depth > 0, continue
    emit_load(3); emit_push(0); emit_gt(); emit_jnz(LBL_BWD_LOOP)
    emit_jmp(LBL_NEXT)

    # Default: unknown instruction, skip
    emit_label(LBL_CLOSE)

    # ── Advance ip and loop back ────────────────────────────────────
    emit_label(LBL_NEXT)
    emit_inc(0)     # ip++
    emit_jmp(LBL_LOOP)

    # ── Exit ────────────────────────────────────────────────────────
    emit_label(LBL_EXIT)
    emit_halt()

    mnm_source = "\n".join(lines) + "\n"
    sidecar = {
        "strings": [],
        "variables": variables,
        "inputs": {"int": [], "str": []},
    }
    info = {
        "bf_source": bf_source,
        "bf_encoded": bf_encoded,
        "prog_len": prog_len,
        "tape_size": tape_size,
        "num_vars": num_vars,
        "prog_base": PROG_BASE,
        "tape_base": TAPE_BASE,
        "mnm_lines": len(lines),
        "num_labels": label_counter[0],
    }
    return mnm_source, sidecar, info


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate_mnm_bf.py 'BF_PROGRAM' [--run]")
        sys.exit(1)

    bf_source = sys.argv[1]
    do_run = "--run" in sys.argv

    mnm_src, sidecar, info = generate_mnm_bf(bf_source)

    mnm_path = "mnm_examples/bf_gen.mnm"
    json_path = "mnm_examples/bf_gen.mnm.json"
    arnoldc_path = "mnm_bf_gen.arnoldc"

    with open(mnm_path, "w") as f:
        f.write(mnm_src)
    with open(json_path, "w") as f:
        json.dump(sidecar, f, indent=2)

    print(f"BF program:     {bf_source}")
    print(f"BF encoded:     {info['bf_encoded']}")
    print(f"MnM lines:      {info['mnm_lines']}")
    print(f"MnM labels:     {info['num_labels']}")
    print(f"MnM variables:  {info['num_vars']} (prog@{info['prog_base']}, tape@{info['tape_base']})")
    print(f"Wrote: {mnm_path}, {json_path}")

    if do_run:
        BASE = os.path.dirname(os.path.abspath(__file__))
        JAR = os.path.join(BASE, "ArnoldC.jar")

        # Step 1: MnM → ArnoldC
        print(f"\n── Generating ArnoldC from MnM ──")
        r = subprocess.run(
            ["python3", "generate_mnm_interpreter.py", mnm_path, json_path, arnoldc_path],
            capture_output=True, text=True,
        )
        print(r.stdout.strip())
        if r.returncode != 0:
            print(f"FAILED: {r.stderr.strip()}")
            sys.exit(1)

        # Step 2: Compile ArnoldC
        print(f"\n── Compiling ArnoldC ──")
        r = subprocess.run(
            ["java", "-jar", JAR, arnoldc_path],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            print(f"COMPILE FAILED: {r.stderr.strip()}")
            sys.exit(1)
        print("Compiled OK")

        # Step 3: Run
        print(f"\n── Running ArnoldC (interpreting MnM interpreting BF) ──")
        class_name = arnoldc_path.replace(".arnoldc", "")
        r = subprocess.run(
            ["java", class_name],
            capture_output=True, text=True, timeout=30,
        )
        if r.returncode != 0:
            print(f"RUNTIME FAILED: {r.stderr.strip()}")
            sys.exit(1)
        print(f"Output:\n{r.stdout.strip()}")
