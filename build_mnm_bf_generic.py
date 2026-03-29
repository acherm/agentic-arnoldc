#!/usr/bin/env python3
"""Build a GENERIC MnM BF interpreter — reads any BF program from MnM input queue.

Unlike generate_mnm_bf.py (which compiles one BF program into MnM variables),
this generates a FIXED MnM BF interpreter that reads the BF program AND its
input from the MnM input queue at runtime.

The output is always the same .mnm file regardless of the BF program.
At runtime, the MnM input queue contains: progLen, opcodes..., bf_input...

This is the MnM layer for Path 6: a truly generic triple chain.

Fixed limits:
  PROG_SLOTS = 120  (max BF instructions, covers Hello World)
  TAPE_SLOTS = 20   (max BF tape cells)

Variable layout:
  var 0:  ip (BF instruction pointer)
  var 1:  dp (BF data pointer)
  var 2:  prog_len
  var 3:  depth (bracket matching)
  var 4:  cur_inst
  var 5:  cur_val
  var 6..6+P-1:   BF program (P slots)
  var 6+P..6+P+T-1: BF tape (T slots)

MnM input queue protocol:
  1. prog_len
  2. prog_len × opcode (encoded: >=1 <=2 +=3 -=4 .=5 ,=6 [=7 ]=8)
  3. bf_input values (consumed by BF , instructions)
"""

import sys

PROG_SLOTS = 120
TAPE_SLOTS = 20


def mnm_token(color, value):
    return color * (value + 1)


def build():
    PROG_BASE = 6
    TAPE_BASE = PROG_BASE + PROG_SLOTS
    NUM_VARS = TAPE_BASE + TAPE_SLOTS

    lines = []
    label_counter = [0]

    def fresh_label():
        label_counter[0] += 1
        return label_counter[0]

    def emit(line):
        lines.append(line)

    def emit_label(lid): emit(f"N {mnm_token('B', lid)}")
    def emit_jmp(lid):   emit(f"B {mnm_token('B', lid)}")
    def emit_jz(lid):    emit(f"BB {mnm_token('B', lid)}")
    def emit_jnz(lid):   emit(f"BBB {mnm_token('B', lid)}")
    def emit_push(val):  emit(f"G {mnm_token('R', val)}")
    def emit_load(v):    emit(f"GG {mnm_token('G', v)}")
    def emit_store(v):   emit(f"GGG {mnm_token('G', v)}")
    def emit_inc(v):     emit(f"GGGGGG {mnm_token('G', v)}")
    def emit_dec(v):     emit(f"GGGGGGG {mnm_token('G', v)}")
    def emit_dup():      emit("GGGG")
    def emit_pop():      emit("GGGGG")
    def emit_eq():       emit("YYYYYY")
    def emit_lt():       emit("YYYYYYY")
    def emit_gt():       emit("YYYYYYYY")
    def emit_print():    emit("O")
    def emit_read_int(): emit("OOO O")
    def emit_halt():     emit("BBBBBB")

    def emit_read_array(base, size, result_var):
        """Read array[TOS] into result_var. Consumes TOS."""
        emit_push(0)
        emit_store(result_var)
        for i in range(size):
            lbl = fresh_label()
            emit_dup()
            emit_push(i)
            emit_eq()
            emit_jz(lbl)
            emit_load(base + i)
            emit_store(result_var)
            emit_label(lbl)
        emit_pop()

    def emit_write_array(base, size, value_var):
        """Write value_var into array[TOS]. Consumes TOS."""
        for i in range(size):
            lbl = fresh_label()
            emit_dup()
            emit_push(i)
            emit_eq()
            emit_jz(lbl)
            emit_load(value_var)
            emit_store(base + i)
            emit_label(lbl)
        emit_pop()

    # ═══════════════════════════════════════════════════════════════
    # PHASE 1: Load BF program from input queue
    # ═══════════════════════════════════════════════════════════════

    # Read prog_len
    emit_read_int()
    emit_store(2)

    # readIdx = 0
    emit_push(0)
    emit_store(0)

    LBL_LOAD = fresh_label()
    LBL_LOAD_DONE = fresh_label()

    emit_label(LBL_LOAD)
    emit_load(0)    # readIdx
    emit_load(2)    # prog_len
    emit_lt()       # readIdx < prog_len?
    emit_jz(LBL_LOAD_DONE)

    # Read one opcode
    emit_read_int()
    emit_store(4)   # cur_inst = opcode

    # Store into program[readIdx] = var[PROG_BASE + readIdx]
    emit_load(0)    # push readIdx
    emit_write_array(PROG_BASE, PROG_SLOTS, 4)

    emit_inc(0)     # readIdx++
    emit_jmp(LBL_LOAD)
    emit_label(LBL_LOAD_DONE)

    # Reset ip = 0
    emit_push(0)
    emit_store(0)

    # ═══════════════════════════════════════════════════════════════
    # PHASE 2: Execute BF program (same structure as generate_mnm_bf)
    # ═══════════════════════════════════════════════════════════════

    LBL_LOOP = fresh_label()
    LBL_EXIT = fresh_label()
    LBL_NEXT = fresh_label()
    LBL_PLUS = fresh_label()
    LBL_MINUS = fresh_label()
    LBL_RIGHT = fresh_label()
    LBL_LEFT = fresh_label()
    LBL_DOT = fresh_label()
    LBL_COMMA = fresh_label()
    LBL_OPEN = fresh_label()
    LBL_CLOSE = fresh_label()

    emit_label(LBL_LOOP)

    # if ip >= prog_len: exit
    emit_load(0)
    emit_load(2)
    emit_lt()
    emit_jz(LBL_EXIT)

    # Fetch program[ip]
    emit_load(0)
    emit_read_array(PROG_BASE, PROG_SLOTS, 4)

    # End marker
    emit_load(4); emit_push(0); emit_eq(); emit_jnz(LBL_EXIT)

    # ── + (3) ──
    emit_load(4); emit_push(3); emit_eq(); emit_jz(LBL_PLUS)
    emit_load(1)
    emit_read_array(TAPE_BASE, TAPE_SLOTS, 5)
    emit_inc(5)
    emit_load(1)
    emit_write_array(TAPE_BASE, TAPE_SLOTS, 5)
    emit_jmp(LBL_NEXT)

    # ── - (4) ──
    emit_label(LBL_PLUS)
    emit_load(4); emit_push(4); emit_eq(); emit_jz(LBL_MINUS)
    emit_load(1)
    emit_read_array(TAPE_BASE, TAPE_SLOTS, 5)
    emit_dec(5)
    emit_load(1)
    emit_write_array(TAPE_BASE, TAPE_SLOTS, 5)
    emit_jmp(LBL_NEXT)

    # ── > (1) ──
    emit_label(LBL_MINUS)
    emit_load(4); emit_push(1); emit_eq(); emit_jz(LBL_RIGHT)
    emit_inc(1)
    emit_jmp(LBL_NEXT)

    # ── < (2) ──
    emit_label(LBL_RIGHT)
    emit_load(4); emit_push(2); emit_eq(); emit_jz(LBL_LEFT)
    emit_dec(1)
    emit_jmp(LBL_NEXT)

    # ── . (5) ──
    emit_label(LBL_LEFT)
    emit_load(4); emit_push(5); emit_eq(); emit_jz(LBL_DOT)
    emit_load(1)
    emit_read_array(TAPE_BASE, TAPE_SLOTS, 5)
    emit_load(5)
    emit_print()
    emit_jmp(LBL_NEXT)

    # ── , (6) ──
    emit_label(LBL_DOT)
    emit_load(4); emit_push(6); emit_eq(); emit_jz(LBL_COMMA)
    emit_read_int()
    emit_store(5)
    emit_load(1)
    emit_write_array(TAPE_BASE, TAPE_SLOTS, 5)
    emit_jmp(LBL_NEXT)

    # ── [ (7) ──
    emit_label(LBL_COMMA)
    emit_load(4); emit_push(7); emit_eq(); emit_jz(LBL_OPEN)
    emit_load(1)
    emit_read_array(TAPE_BASE, TAPE_SLOTS, 5)
    emit_load(5); emit_push(0); emit_eq()
    emit_jz(LBL_NEXT)  # non-zero → continue
    # Zero → forward scan
    emit_push(1); emit_store(3)
    LBL_FWD = fresh_label()
    LBL_FWD_NO = fresh_label()
    LBL_FWD_NC = fresh_label()
    emit_label(LBL_FWD)
    emit_inc(0)
    emit_load(0)
    emit_read_array(PROG_BASE, PROG_SLOTS, 4)
    emit_load(4); emit_push(7); emit_eq(); emit_jz(LBL_FWD_NO)
    emit_inc(3)
    emit_label(LBL_FWD_NO)
    emit_load(4); emit_push(8); emit_eq(); emit_jz(LBL_FWD_NC)
    emit_dec(3)
    emit_label(LBL_FWD_NC)
    emit_load(3); emit_push(0); emit_gt(); emit_jnz(LBL_FWD)
    emit_jmp(LBL_NEXT)

    # ── ] (8) ──
    emit_label(LBL_OPEN)
    emit_load(4); emit_push(8); emit_eq(); emit_jz(LBL_CLOSE)
    emit_load(1)
    emit_read_array(TAPE_BASE, TAPE_SLOTS, 5)
    emit_load(5); emit_push(0); emit_eq()
    emit_jnz(LBL_NEXT)  # zero → continue
    # Non-zero → backward scan
    emit_push(1); emit_store(3)
    LBL_BWD = fresh_label()
    LBL_BWD_NC = fresh_label()
    LBL_BWD_NO = fresh_label()
    emit_label(LBL_BWD)
    emit_dec(0)
    emit_load(0)
    emit_read_array(PROG_BASE, PROG_SLOTS, 4)
    emit_load(4); emit_push(8); emit_eq(); emit_jz(LBL_BWD_NC)
    emit_inc(3)
    emit_label(LBL_BWD_NC)
    emit_load(4); emit_push(7); emit_eq(); emit_jz(LBL_BWD_NO)
    emit_dec(3)
    emit_label(LBL_BWD_NO)
    emit_load(3); emit_push(0); emit_gt(); emit_jnz(LBL_BWD)
    emit_jmp(LBL_NEXT)

    # ── default ──
    emit_label(LBL_CLOSE)

    # ── advance ip, loop ──
    emit_label(LBL_NEXT)
    emit_inc(0)
    emit_jmp(LBL_LOOP)

    # ── exit ──
    emit_label(LBL_EXIT)
    emit_halt()

    mnm_source = "\n".join(lines) + "\n"

    # Sidecar: all variables initialized to 0, no pre-loaded inputs
    sidecar = {
        "strings": [],
        "variables": [0] * NUM_VARS,
        "inputs": {"int": [], "str": []},
    }

    info = {
        "mnm_lines": len(lines),
        "num_vars": NUM_VARS,
        "prog_slots": PROG_SLOTS,
        "tape_slots": TAPE_SLOTS,
        "num_labels": label_counter[0],
    }

    return mnm_source, sidecar, info


if __name__ == "__main__":
    import json

    mnm_src, sidecar, info = build()

    out_mnm = sys.argv[1] if len(sys.argv) > 1 else "mnm_bf_generic.mnm"
    out_json = out_mnm.replace('.mnm', '.mnm.json')

    with open(out_mnm, 'w') as f:
        f.write(mnm_src)
    with open(out_json, 'w') as f:
        json.dump(sidecar, f)

    print(f"Built generic MnM BF interpreter:")
    print(f"  {info['mnm_lines']} MnM instructions, {info['num_vars']} variables")
    print(f"  {info['num_labels']} labels")
    print(f"  PROG_SLOTS={info['prog_slots']}, TAPE_SLOTS={info['tape_slots']}")
    print(f"  → {out_mnm}, {out_json}")
