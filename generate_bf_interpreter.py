#!/usr/bin/env python3
"""Generate an ArnoldC Brainfuck interpreter.

The generated program embeds a BF program as integer-coded instructions
and interprets it using simulated tape and instruction pointer.

Encoding: >=1 <=2 +=3 -=4 .=5 ,=6 [=7 ]=8 end=0

Can be used as a module:
    from generate_bf_interpreter import generate
    generate("+++[>++<-]>.", output_path="out.arnoldc")

Or as a standalone script:
    python3 generate_bf_interpreter.py
"""

ENCODING = {'>': 1, '<': 2, '+': 3, '-': 4, '.': 5, ',': 6, '[': 7, ']': 8}


def estimate_tape_size(bf_source):
    """Estimate the maximum tape cell index touched by a BF program."""
    pos = 0
    max_pos = 0
    for c in bf_source:
        if c == '>':
            pos += 1
            max_pos = max(max_pos, pos)
        elif c == '<':
            pos -= 1
    return max_pos + 1


def generate(bf_source, prog_size=None, tape_size=None, output_path=None):
    """Generate an ArnoldC Brainfuck interpreter with the given BF program embedded.

    Args:
        bf_source: The Brainfuck source code to embed.
        prog_size: Number of program slots. Auto-calculated if None.
        tape_size: Number of tape cells. Auto-calculated if None.
        output_path: Path to write the .arnoldc file. If None, doesn't write.

    Returns:
        The generated ArnoldC source code as a string.
    """
    bf_encoded = [ENCODING[c] for c in bf_source if c in ENCODING]

    if prog_size is None:
        prog_size = len(bf_encoded) + 1  # +1 for end marker
    if tape_size is None:
        tape_size = max(estimate_tape_size(bf_source) + 2, 3)

    if prog_size > 254:
        raise ValueError(f"prog_size={prog_size} exceeds JVM 254-parameter limit")
    if tape_size > 254:
        raise ValueError(f"tape_size={tape_size} exceeds JVM 254-parameter limit")
    if len(bf_encoded) >= prog_size:
        raise ValueError(f"BF program has {len(bf_encoded)} instructions but prog_size={prog_size}")

    padded = bf_encoded + [0] * (prog_size - len(bf_encoded))

    lines = []

    def emit(s=""):
        lines.append(s)

    # ===== MAIN PROGRAM =====
    emit("IT'S SHOWTIME")
    emit()

    # Tape cells
    for i in range(tape_size):
        emit(f"HEY CHRISTMAS TREE c{i}")
        emit("YOU SET US UP 0")
    emit()

    # NOTE: Program instructions are NOT stored as main variables.
    # They are hardcoded as constants inside the fetch() method.
    # This avoids the ArnoldC 100-local-variable limit in main.

    # Control variables
    ctrl_vars = [
        ("dp", 0), ("ip", 0), ("inst", 0), ("curVal", 0),
        ("writeBack", 0), ("advanced", 0), ("isInst", 0),
        ("isZero", 0), ("isNotZero", 0), ("needScanFwd", 0),
        ("needScanBwd", 0), ("scanCond", 0), ("depth", 0),
        ("notAdvanced", 0), ("running", 1),
    ]
    for name, val in ctrl_vars:
        emit(f"HEY CHRISTMAS TREE {name}")
        emit(f"YOU SET US UP {val}")
    emit()

    c_args = " ".join(f"c{i}" for i in range(tape_size))

    # ===== MAIN EXECUTION LOOP =====
    emit("STICK AROUND running")
    emit()

    # Fetch instruction at ip
    emit("GET YOUR ASS TO MARS inst")
    emit("DO IT NOW fetch ip")
    emit()

    # Check if end of program (inst == 0)
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 0")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE isInst")
    emit("GET TO THE CHOPPER running")
    emit("HERE IS MY INVITATION 0")
    emit("ENOUGH TALK")
    emit("YOU HAVE NO RESPECT FOR LOGIC")
    emit()

    # Reset flags
    emit("GET TO THE CHOPPER writeBack")
    emit("HERE IS MY INVITATION 0")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER advanced")
    emit("HERE IS MY INVITATION 0")
    emit("ENOUGH TALK")
    emit()

    # Read current cell value
    emit("GET YOUR ASS TO MARS curVal")
    emit(f"DO IT NOW tapeRead dp {c_args}")
    emit()

    # Compute isZero and isNotZero
    emit("GET TO THE CHOPPER isZero")
    emit("HERE IS MY INVITATION curVal")
    emit("YOU ARE NOT YOU YOU ARE ME 0")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER isNotZero")
    emit("HERE IS MY INVITATION 1")
    emit("GET DOWN isZero")
    emit("ENOUGH TALK")
    emit()

    # --- Instruction dispatch ---

    # Handle + (inst == 3): increment cell
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 3")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE isInst")
    emit("GET TO THE CHOPPER curVal")
    emit("HERE IS MY INVITATION curVal")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER writeBack")
    emit("HERE IS MY INVITATION 1")
    emit("ENOUGH TALK")
    emit("YOU HAVE NO RESPECT FOR LOGIC")
    emit()

    # Handle - (inst == 4): decrement cell
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 4")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE isInst")
    emit("GET TO THE CHOPPER curVal")
    emit("HERE IS MY INVITATION curVal")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER writeBack")
    emit("HERE IS MY INVITATION 1")
    emit("ENOUGH TALK")
    emit("YOU HAVE NO RESPECT FOR LOGIC")
    emit()

    # Handle > (inst == 1): move data pointer right
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 1")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE isInst")
    emit("GET TO THE CHOPPER dp")
    emit("HERE IS MY INVITATION dp")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit("YOU HAVE NO RESPECT FOR LOGIC")
    emit()

    # Handle < (inst == 2): move data pointer left
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 2")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE isInst")
    emit("GET TO THE CHOPPER dp")
    emit("HERE IS MY INVITATION dp")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("YOU HAVE NO RESPECT FOR LOGIC")
    emit()

    # Handle . (inst == 5): print current cell
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 5")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE isInst")
    emit("TALK TO THE HAND curVal")
    emit("YOU HAVE NO RESPECT FOR LOGIC")
    emit()

    # --- Bracket handling ---
    # Compute scan flags BEFORE any scanning modifies inst
    # needScanFwd = (inst == 7) AND (curVal == 0)
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 7")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER needScanFwd")
    emit("HERE IS MY INVITATION isInst")
    emit("KNOCK KNOCK isZero")
    emit("ENOUGH TALK")
    emit()

    # needScanBwd = (inst == 8) AND (curVal != 0)
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 8")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER needScanBwd")
    emit("HERE IS MY INVITATION isInst")
    emit("KNOCK KNOCK isNotZero")
    emit("ENOUGH TALK")
    emit()

    # --- Forward scan: [ with cell==0, skip to matching ] ---
    emit("BECAUSE I'M GOING TO SAY PLEASE needScanFwd")
    emit("GET TO THE CHOPPER depth")
    emit("HERE IS MY INVITATION 1")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER ip")
    emit("HERE IS MY INVITATION ip")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit("YOU HAVE NO RESPECT FOR LOGIC")
    emit()

    # Forward scan loop
    emit("GET TO THE CHOPPER scanCond")
    emit("HERE IS MY INVITATION needScanFwd")
    emit("ENOUGH TALK")
    emit("STICK AROUND scanCond")
    emit("GET YOUR ASS TO MARS inst")
    emit("DO IT NOW fetch ip")
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 7")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE isInst")
    emit("GET TO THE CHOPPER depth")
    emit("HERE IS MY INVITATION depth")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit("YOU HAVE NO RESPECT FOR LOGIC")
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 8")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE isInst")
    emit("GET TO THE CHOPPER depth")
    emit("HERE IS MY INVITATION depth")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("YOU HAVE NO RESPECT FOR LOGIC")
    emit("GET TO THE CHOPPER scanCond")
    emit("HERE IS MY INVITATION depth")
    emit("LET OFF SOME STEAM BENNET 0")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE scanCond")
    emit("GET TO THE CHOPPER ip")
    emit("HERE IS MY INVITATION ip")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit("YOU HAVE NO RESPECT FOR LOGIC")
    emit("CHILL")
    emit()

    # --- Backward scan: ] with cell!=0, jump back to matching [ ---
    emit("BECAUSE I'M GOING TO SAY PLEASE needScanBwd")
    emit("GET TO THE CHOPPER depth")
    emit("HERE IS MY INVITATION 1")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER ip")
    emit("HERE IS MY INVITATION ip")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("GET TO THE CHOPPER advanced")
    emit("HERE IS MY INVITATION 1")
    emit("ENOUGH TALK")
    emit("YOU HAVE NO RESPECT FOR LOGIC")
    emit()

    # Backward scan loop
    emit("GET TO THE CHOPPER scanCond")
    emit("HERE IS MY INVITATION needScanBwd")
    emit("ENOUGH TALK")
    emit("STICK AROUND scanCond")
    emit("GET YOUR ASS TO MARS inst")
    emit("DO IT NOW fetch ip")
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 8")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE isInst")
    emit("GET TO THE CHOPPER depth")
    emit("HERE IS MY INVITATION depth")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit("YOU HAVE NO RESPECT FOR LOGIC")
    emit("GET TO THE CHOPPER isInst")
    emit("HERE IS MY INVITATION inst")
    emit("YOU ARE NOT YOU YOU ARE ME 7")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE isInst")
    emit("GET TO THE CHOPPER depth")
    emit("HERE IS MY INVITATION depth")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("YOU HAVE NO RESPECT FOR LOGIC")
    emit("GET TO THE CHOPPER scanCond")
    emit("HERE IS MY INVITATION depth")
    emit("LET OFF SOME STEAM BENNET 0")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE scanCond")
    emit("GET TO THE CHOPPER ip")
    emit("HERE IS MY INVITATION ip")
    emit("GET DOWN 1")
    emit("ENOUGH TALK")
    emit("YOU HAVE NO RESPECT FOR LOGIC")
    emit("CHILL")
    emit()

    # --- Write back modified cell if needed ---
    emit("BECAUSE I'M GOING TO SAY PLEASE writeBack")
    for i in range(tape_size):
        emit(f"GET YOUR ASS TO MARS c{i}")
        emit(f"DO IT NOW tapeWrite dp {i} c{i} curVal")
    emit("YOU HAVE NO RESPECT FOR LOGIC")
    emit()

    # --- Advance instruction pointer if not already done ---
    emit("GET TO THE CHOPPER notAdvanced")
    emit("HERE IS MY INVITATION 1")
    emit("GET DOWN advanced")
    emit("ENOUGH TALK")
    emit("BECAUSE I'M GOING TO SAY PLEASE notAdvanced")
    emit("GET TO THE CHOPPER ip")
    emit("HERE IS MY INVITATION ip")
    emit("GET UP 1")
    emit("ENOUGH TALK")
    emit("YOU HAVE NO RESPECT FOR LOGIC")
    emit()

    # End main loop
    emit("CHILL")
    emit()

    # --- Post-execution: dump tape state ---
    emit('TALK TO THE HAND "---"')
    emit('TALK TO THE HAND "TAPE"')
    for i in range(tape_size):
        emit(f"TALK TO THE HAND c{i}")
    emit('TALK TO THE HAND "DP"')
    emit("TALK TO THE HAND dp")
    emit()

    emit("YOU HAVE BEEN TERMINATED")
    emit()

    # ===== METHOD: fetch =====
    # Program instructions are hardcoded as constants (not parameters).
    # This allows programs of any size without hitting the 100-local limit.
    emit("LISTEN TO ME VERY CAREFULLY fetch")
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
        emit(f"HERE IS MY INVITATION {padded[i]}")
        emit("ENOUGH TALK")
        emit("YOU HAVE NO RESPECT FOR LOGIC")
    emit("I'LL BE BACK result")
    emit("HASTA LA VISTA, BABY")
    emit()

    # ===== METHOD: tapeRead =====
    emit("LISTEN TO ME VERY CAREFULLY tapeRead")
    emit("I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE idx")
    for i in range(tape_size):
        emit(f"I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE v{i}")
    emit("GIVE THESE PEOPLE AIR")
    emit("HEY CHRISTMAS TREE result")
    emit("YOU SET US UP 0")
    emit("HEY CHRISTMAS TREE eq")
    emit("YOU SET US UP 0")
    for i in range(tape_size):
        emit("GET TO THE CHOPPER eq")
        emit("HERE IS MY INVITATION idx")
        emit(f"YOU ARE NOT YOU YOU ARE ME {i}")
        emit("ENOUGH TALK")
        emit("BECAUSE I'M GOING TO SAY PLEASE eq")
        emit("GET TO THE CHOPPER result")
        emit(f"HERE IS MY INVITATION v{i}")
        emit("ENOUGH TALK")
        emit("YOU HAVE NO RESPECT FOR LOGIC")
    emit("I'LL BE BACK result")
    emit("HASTA LA VISTA, BABY")
    emit()

    # ===== METHOD: tapeWrite =====
    emit("LISTEN TO ME VERY CAREFULLY tapeWrite")
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
    emit("YOU HAVE NO RESPECT FOR LOGIC")
    emit("I'LL BE BACK result")
    emit("HASTA LA VISTA, BABY")

    source = "\n".join(lines) + "\n"

    if output_path:
        with open(output_path, "w") as f:
            f.write(source)

    return source


if __name__ == "__main__":
    import os
    bf_source = "+++[>++<-]>."
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brainfuck.arnoldc")
    source = generate(bf_source, output_path=out)
    n_lines = source.count("\n")
    encoded = [ENCODING[c] for c in bf_source if c in ENCODING]
    print(f"Generated {n_lines} lines -> brainfuck.arnoldc")
    print(f"Embedded BF program: {bf_source}")
    print(f"Encoded as: {encoded}")
