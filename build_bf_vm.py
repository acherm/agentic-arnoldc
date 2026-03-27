#!/usr/bin/env python3
"""Build a fixed Brainfuck interpreter in ArnoldC that reads BF from stdin.

Unlike brainfuck.arnoldc (which hardcodes one BF program), this generates
a single fixed ArnoldC program that reads ANY BF program from stdin and
executes it. No Python needed at runtime.

Requires the patched ArnoldC compiler (static fields + shared Scanner).

Fixed limits:
  PROG_SIZE = 200  (max BF instructions)
  TAPE_SIZE = 150  (max tape cells)

Input protocol (integers from stdin):
  1. progLen               (number of BF instructions)
  2. progLen × opcode      (encoded: >=1 <=2 +=3 -=4 .=5 ,=6 [=7 ]=8)

Usage:
  python3 build_bf_vm.py                         # generates bf_vm.arnoldc
  java -jar ArnoldC-patched.jar bf_vm.arnoldc    # compile once
  echo "12 3 3 3 7 1 3 3 2 4 8 1 5" | java bf_vm  # run +++[>++<-]>. → 6
"""

import sys

PROG_SIZE = 200
TAPE_SIZE = 150


def build():
    lines = []
    def emit(s=""):
        lines.append(s)
    def emit_end_if():
        emit("YOU HAVE NO RESPECT FOR LOGIC")

    # ═════════════════════════════════════════════════════════════════
    # A. DECLARATIONS
    # ═════════════════════════════════════════════════════════════════
    emit("IT'S SHOWTIME")
    emit()

    # Program storage
    for i in range(PROG_SIZE):
        emit(f"HEY CHRISTMAS TREE p{i}")
        emit("YOU SET US UP 0")
    emit()

    # Tape
    for i in range(TAPE_SIZE):
        emit(f"HEY CHRISTMAS TREE t{i}")
        emit("YOU SET US UP 0")
    emit()

    # Control
    ctrl = [
        ("ip", 0), ("dp", 0), ("inst", 0), ("curVal", 0),
        ("progLen", 0), ("running", 1),
        ("isInst", 0), ("depth", 0), ("scanCond", 0),
        ("a", 0), ("readIdx", 0), ("readCond", 0),
    ]
    for name, val in ctrl:
        emit(f"HEY CHRISTMAS TREE {name}")
        emit(f"YOU SET US UP {val}")
    emit()

    # ═════════════════════════════════════════════════════════════════
    # B. READ PROGRAM FROM STDIN
    # ═════════════════════════════════════════════════════════════════
    def emit_read_into(var):
        emit(f"GET YOUR ASS TO MARS {var}")
        emit("DO IT NOW")
        emit("I WANT TO ASK YOU A BUNCH OF QUESTIONS AND I WANT TO HAVE THEM ANSWERED IMMEDIATELY")

    emit_read_into("progLen")

    emit("GET TO THE CHOPPER readIdx")
    emit("HERE IS MY INVITATION 0")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER readCond")
    emit("HERE IS MY INVITATION progLen")
    emit("LET OFF SOME STEAM BENNET readIdx")
    emit("ENOUGH TALK")
    emit("STICK AROUND readCond")
    emit_read_into("a")
    emit("DO IT NOW progW readIdx a")
    emit("GET TO THE CHOPPER readIdx")
    emit("HERE IS MY INVITATION readIdx")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER readCond")
    emit("HERE IS MY INVITATION progLen")
    emit("LET OFF SOME STEAM BENNET readIdx")
    emit("ENOUGH TALK")
    emit("CHILL")
    emit()

    # ═════════════════════════════════════════════════════════════════
    # C. MAIN EXECUTION LOOP
    # ═════════════════════════════════════════════════════════════════
    emit("STICK AROUND running")
    emit()

    # Fetch instruction
    emit("GET YOUR ASS TO MARS inst")
    emit("DO IT NOW progR ip")
    emit()

    # End of program (inst == 0 or ip >= progLen)
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 0")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE isInst")
    emit("GET TO THE CHOPPER running")
    emit("HERE IS MY INVITATION 0")
    emit("ENOUGH TALK")
    emit_end_if()
    emit()

    # Read current tape cell
    emit("GET YOUR ASS TO MARS curVal")
    emit("DO IT NOW tapeR dp")
    emit()

    # ── + (inst == 3): increment cell ──────────────────────────
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 3")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE isInst")
    emit("GET TO THE CHOPPER curVal")
    emit("HERE IS MY INVITATION curVal")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit("DO IT NOW tapeW dp curVal")
    emit_end_if()
    emit()

    # ── - (inst == 4): decrement cell ──────────────────────────
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 4")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE isInst")
    emit("GET TO THE CHOPPER curVal")
    emit("HERE IS MY INVITATION curVal")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("DO IT NOW tapeW dp curVal")
    emit_end_if()
    emit()

    # ── > (inst == 1): move right ─────────────────────────────
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 1")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE isInst")
    emit("GET TO THE CHOPPER dp")
    emit("HERE IS MY INVITATION dp")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit_end_if()
    emit()

    # ── < (inst == 2): move left ──────────────────────────────
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 2")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE isInst")
    emit("GET TO THE CHOPPER dp")
    emit("HERE IS MY INVITATION dp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit_end_if()
    emit()

    # ── . (inst == 5): print cell ─────────────────────────────
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 5")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE isInst")
    emit("TALK TO THE HAND curVal")
    emit_end_if()
    emit()

    # ── [ (inst == 7): forward scan if zero ────────────────────
    # Compute: isInst = (inst == 7) AND (curVal == 0)
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 7")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER a")
    emit("HERE IS MY INVITATION curVal")
    emit("YOU ARE NOT YOU YOU ARE ME 0")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION isInst")
    emit("KNOCK KNOCK a")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE isInst")
    # Forward scan for matching ]
    emit("GET TO THE CHOPPER depth")
    emit("HERE IS MY INVITATION 1")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER scanCond")
    emit("HERE IS MY INVITATION depth")
    emit("LET OFF SOME STEAM BENNET 0")
    emit("ENOUGH TALK")
    emit("STICK AROUND scanCond")
    emit("GET TO THE CHOPPER ip")
    emit("HERE IS MY INVITATION ip")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS inst")
    emit("DO IT NOW progR ip")
    # if [, depth++
    emit("GET TO THE CHOPPER a")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 7")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE a")
    emit("GET TO THE CHOPPER depth")
    emit("HERE IS MY INVITATION depth")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit_end_if()
    # if ], depth--
    emit("GET TO THE CHOPPER a")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 8")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE a")
    emit("GET TO THE CHOPPER depth")
    emit("HERE IS MY INVITATION depth")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit_end_if()
    emit("GET TO THE CHOPPER scanCond")
    emit("HERE IS MY INVITATION depth")
    emit("LET OFF SOME STEAM BENNET 0")
    emit("ENOUGH TALK")
    emit("CHILL")
    emit_end_if()
    emit()

    # ── ] (inst == 8): backward scan if non-zero ──────────────
    # Compute: isInst = (inst == 8) AND (curVal != 0)
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 8")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER a")
    emit("HERE IS MY INVITATION curVal")
    emit("YOU ARE NOT YOU YOU ARE ME 0")
    emit("ENOUGH TALK")
    # a = (curVal == 0), we want NOT a
    emit("GET TO THE CHOPPER a")
    emit("HERE IS MY INVITATION 1")
    emit("GET DOWN a")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION isInst")
    emit("KNOCK KNOCK a")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE isInst")
    # Backward scan for matching [
    emit("GET TO THE CHOPPER depth")
    emit("HERE IS MY INVITATION 1")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER scanCond")
    emit("HERE IS MY INVITATION depth")
    emit("LET OFF SOME STEAM BENNET 0")
    emit("ENOUGH TALK")
    emit("STICK AROUND scanCond")
    emit("GET TO THE CHOPPER ip")
    emit("HERE IS MY INVITATION ip")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET YOUR ASS TO MARS inst")
    emit("DO IT NOW progR ip")
    # if ], depth++
    emit("GET TO THE CHOPPER a")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 8")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE a")
    emit("GET TO THE CHOPPER depth")
    emit("HERE IS MY INVITATION depth")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit_end_if()
    # if [, depth--
    emit("GET TO THE CHOPPER a")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 7")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE a")
    emit("GET TO THE CHOPPER depth")
    emit("HERE IS MY INVITATION depth")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit_end_if()
    emit("GET TO THE CHOPPER scanCond")
    emit("HERE IS MY INVITATION depth")
    emit("LET OFF SOME STEAM BENNET 0")
    emit("ENOUGH TALK")
    emit("CHILL")
    emit_end_if()
    emit()

    # Advance ip
    emit("GET TO THE CHOPPER ip")
    emit("HERE IS MY INVITATION ip")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit()

    emit("CHILL")
    emit()
    emit("YOU HAVE BEEN TERMINATED")
    emit()

    # ═════════════════════════════════════════════════════════════════
    # D. METHODS
    # ═════════════════════════════════════════════════════════════════

    CHUNK = 2000

    def emit_read_method(name, prefix, size):
        """Non-void: name(idx) → prefix[idx], with auto-splitting."""
        def emit_chunk(cname, start, end):
            emit(f"LISTEN TO ME VERY CAREFULLY {cname}")
            emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE idx")
            emit("GIVE THESE PEOPLE AIR")
            emit("HEY CHRISTMAS TREE res")
            emit("YOU SET US UP 0")
            emit("HEY CHRISTMAS TREE eq")
            emit("YOU SET US UP 0")
            for i in range(start, end):
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

        if size <= CHUNK:
            emit_chunk(name, 0, size)
        else:
            chunks = [(s, min(s + CHUNK, size)) for s in range(0, size, CHUNK)]
            emit(f"LISTEN TO ME VERY CAREFULLY {name}")
            emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE idx")
            emit("GIVE THESE PEOPLE AIR")
            emit("HEY CHRISTMAS TREE res")
            emit("YOU SET US UP 0")
            emit("HEY CHRISTMAS TREE gt")
            emit("YOU SET US UP 0")
            for ci in range(len(chunks) - 1, 0, -1):
                start, _ = chunks[ci]
                emit("GET TO THE CHOPPER gt")
                emit("HERE IS MY INVITATION idx")
                emit(f"LET OFF SOME STEAM BENNET {start - 1}")
                emit("ENOUGH TALK")
                emit("BECAUSE I'M GOING TO SAY PLEASE gt")
                emit("GET YOUR ASS TO MARS res")
                emit(f"DO IT NOW {name}C{ci} idx")
                emit("BULLSHIT")
            emit("GET YOUR ASS TO MARS res")
            emit(f"DO IT NOW {name}C0 idx")
            for _ in range(len(chunks) - 1):
                emit_end_if()
            emit("I'LL BE BACK res")
            emit("HASTA LA VISTA, BABY")
            emit()
            for ci, (start, end) in enumerate(chunks):
                emit_chunk(f"{name}C{ci}", start, end)

    def emit_write_method(name, prefix, size):
        """Void: name(idx, val) → prefix[idx] = val, with auto-splitting."""
        def emit_chunk(cname, start, end):
            emit(f"LISTEN TO ME VERY CAREFULLY {cname}")
            emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE idx")
            emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE val")
            emit("HEY CHRISTMAS TREE eq")
            emit("YOU SET US UP 0")
            for i in range(start, end):
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

        if size <= CHUNK:
            emit_chunk(name, 0, size)
        else:
            chunks = [(s, min(s + CHUNK, size)) for s in range(0, size, CHUNK)]
            emit(f"LISTEN TO ME VERY CAREFULLY {name}")
            emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE idx")
            emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE val")
            emit("HEY CHRISTMAS TREE gt")
            emit("YOU SET US UP 0")
            for ci in range(len(chunks) - 1, 0, -1):
                start, _ = chunks[ci]
                emit("GET TO THE CHOPPER gt")
                emit("HERE IS MY INVITATION idx")
                emit(f"LET OFF SOME STEAM BENNET {start - 1}")
                emit("ENOUGH TALK")
                emit("BECAUSE I'M GOING TO SAY PLEASE gt")
                emit(f"DO IT NOW {name}C{ci} idx val")
                emit("BULLSHIT")
            emit(f"DO IT NOW {name}C0 idx val")
            for _ in range(len(chunks) - 1):
                emit_end_if()
            emit("HASTA LA VISTA, BABY")
            emit()
            for ci, (start, end) in enumerate(chunks):
                emit_chunk(f"{name}C{ci}", start, end)

    emit_read_method("progR", "p", PROG_SIZE)
    emit_write_method("progW", "p", PROG_SIZE)
    emit_read_method("tapeR", "t", TAPE_SIZE)
    emit_write_method("tapeW", "t", TAPE_SIZE)

    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build a fixed BF interpreter in ArnoldC")
    parser.add_argument("output", nargs="?", default="bf_vm.arnoldc")
    parser.add_argument("--prog", type=int, default=PROG_SIZE)
    parser.add_argument("--tape", type=int, default=TAPE_SIZE)
    args = parser.parse_args()
    PROG_SIZE = args.prog
    TAPE_SIZE = args.tape
    source = build()
    with open(args.output, "w") as f:
        f.write(source)
    n = source.count('\n')
    print(f"Built {n} lines → {args.output}")
    print(f"  PROG_SIZE={PROG_SIZE}, TAPE_SIZE={TAPE_SIZE}")
