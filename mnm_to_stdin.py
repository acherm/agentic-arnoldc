#!/usr/bin/env python3
"""Convert a .mnm + .mnm.json into the stdin integer stream for mnm_vm.

Usage:
    python3 mnm_to_stdin.py prog.mnm prog.mnm.json | java mnm_vm
    python3 mnm_to_stdin.py prog.mnm prog.mnm.json --staggered | java mnm_vm
"""

import json
import sys

from generate_mnm_interpreter import parse_mnm, resolve_labels, OPCODES


def mnm_to_stdin(mnm_source, sidecar_data):
    """Convert MnM program to stdin integer stream for mnm_vm."""
    raw = parse_mnm(mnm_source)
    instructions, _ = resolve_labels(raw)

    variables = sidecar_data.get('variables', [])
    int_queues = sidecar_data.get('inputs', {}).get('int', [])
    # Flatten all int queues into one sequence
    flat_inputs = []
    for q in int_queues:
        flat_inputs.extend(q)

    values = []

    # 1. progLen
    values.append(len(instructions))

    # 2. instruction pairs (opcode, operand)
    for op, operand in instructions:
        values.append(OPCODES[op])
        values.append(operand if operand is not None else 0)

    # 3. numVars + initial values
    values.append(len(variables))
    values.extend(variables)

    # 4. numInputs + values
    values.append(len(flat_inputs))
    values.extend(flat_inputs)

    return values


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 mnm_to_stdin.py PROG.mnm PROG.mnm.json [--staggered]")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        mnm_source = f.read()
    with open(sys.argv[2]) as f:
        sidecar = json.load(f)

    values = mnm_to_stdin(mnm_source, sidecar)

    if "--staggered" in sys.argv:
        # Output with sleep for ArnoldC's Scanner quirk
        import time
        for v in values:
            print(v, flush=True)
            time.sleep(0.1)
    else:
        # One value per line
        for v in values:
            print(v)
