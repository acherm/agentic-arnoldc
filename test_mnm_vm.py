#!/usr/bin/env python3
"""Test suite for mnm_vm.arnoldc — the true fixed MnM interpreter.

Each test converts a MnM program to stdin values, pipes them with
staggered delivery to mnm_vm, and checks the output.
"""

import json
import os
import subprocess
import sys
import tempfile

from mnm_to_stdin import mnm_to_stdin
from test_mnm import sidecar

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TIMEOUT = 30
SLEEP = 0.1


def run_test(name, mnm_src, sidecar_data, expected_lines):
    """Feed MnM program to mnm_vm via staggered stdin, check output."""
    values = mnm_to_stdin(mnm_src, sidecar_data)

    # Write values to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        for v in values:
            f.write(f"{v}\n")
        vals_path = f.name

    try:
        # Stagger with bash while-read
        cmd = f'(while IFS= read -r line; do echo "$line"; sleep {SLEEP}; done < {vals_path}) | timeout {TIMEOUT} java mnm_vm'
        r = subprocess.run(
            ['bash', '-c', cmd],
            capture_output=True, text=True, cwd=BASE_DIR,
            timeout=TIMEOUT + len(values) * SLEEP + 5,
        )
        if r.returncode != 0 and r.returncode != 124:  # 124 = timeout
            return "RUNTIME_FAIL", r.stderr.strip()[:100]

        actual = r.stdout.strip().split('\n') if r.stdout.strip() else []
        if actual == expected_lines:
            return "PASS", None
        else:
            return "FAIL", f"expected {expected_lines!r}, got {actual!r}"
    finally:
        os.unlink(vals_path)


# ── Test cases ───────────────────────────────────────────────────────────

TESTS = []

def test(name, mnm_src, sc, expected):
    TESTS.append((name, mnm_src, sc, expected))


# PUSH + PRINT
test("push_print",
     "G RRRRR\nO\nBBBBBB\n",
     sidecar(), ["4"])

# ADD
test("add",
     "G RRRR\nG RRRRRRRR\nY\nO\nBBBBBB\n",
     sidecar(), ["10"])

# SUB
test("sub",
     "G RRRRRRRRRRR\nG RRRR\nYY\nO\nBBBBBB\n",
     sidecar(), ["7"])

# MUL
test("mul",
     "G RRRRRRR\nG RRRRRRRR\nYYY\nO\nBBBBBB\n",
     sidecar(), ["42"])

# EQ true
test("eq_true",
     "G RRRRRR\nG RRRRRR\nYYYYYY\nO\nBBBBBB\n",
     sidecar(), ["1"])

# GT
test("gt_true",
     "G RRRRRRRR\nG RRRR\nYYYYYYYY\nO\nBBBBBB\n",
     sidecar(), ["1"])

# NOT
test("not_zero",
     "G R\nRRRRR\nO\nBBBBBB\n",
     sidecar(), ["1"])

# DUP
test("dup",
     "G RRRRR\nGGGG\nO\nO\nBBBBBB\n",
     sidecar(), ["4", "4"])

# SWAP
test("swap",
     "G RR\nG RRR\nR\nO\nO\nBBBBBB\n",
     sidecar(), ["1", "2"])

# Variables: LOAD/STORE
test("var_load_store",
     "G RRRRRR\nGGG G\nGG G\nO\nBBBBBB\n",
     sidecar(variables=[0]), ["5"])

# INC/DEC
test("inc_dec",
     "GGGGGG G\nGGGGGG G\nGG G\nO\nGGGGGGG G\nGG G\nO\nBBBBBB\n",
     sidecar(variables=[10]), ["12", "11"])

# JMP
test("jmp",
     "B BBB\nG RRRRR\nO\nN BBB\nG RRRR\nO\nBBBBBB\n",
     sidecar(), ["3"])

# JZ taken
test("jz_taken",
     "G R\nBB BB\nG RRRR\nO\nN BB\nG RRR\nO\nBBBBBB\n",
     sidecar(), ["2"])

# JNZ taken
test("jnz_taken",
     "G RR\nBBB BB\nG RRRR\nO\nN BB\nG RRR\nO\nBBBBBB\n",
     sidecar(), ["2"])

# Countdown loop
test("countdown",
     "N B\nGG G\nGGGG\nO\nGGGGGGG G\nGG G\nG R\nYYYYYYYY\nBBB B\nBBBBBB\n",
     sidecar(variables=[3]), ["3", "2", "1"])

# Factorial(5) with READ_INT
test("factorial_5",
     """OOO O
GGG G
G RR
GGG GG
N B
GG G
G RR
YYYYYYYY
BB BB
GG GG
GG G
YYY
GGG GG
GGGGGGG G
B B
N BB
GG GG
O
OOOOOO
BBBBBB
""",
     sidecar(variables=[0, 0], int_inputs=[[5]]),
     ["120"])


# ── Runner ───────────────────────────────────────────────────────────

def main():
    # Check mnm_vm.class exists
    if not os.path.exists(os.path.join(BASE_DIR, "mnm_vm.class")):
        print("mnm_vm.class not found. Compile first:")
        print("  java -jar ArnoldC-patched.jar mnm_vm.arnoldc")
        return 1

    passed = failed = errors = 0

    for name, src, sc, expected in TESTS:
        status, detail = run_test(name, src, sc, expected)
        if status == "PASS":
            passed += 1
            print(f"  PASS  {name}")
        elif status == "FAIL":
            failed += 1
            print(f"  FAIL  {name}: {detail}")
        else:
            errors += 1
            print(f"  ERROR {name}: {detail}")

    total = passed + failed + errors
    print(f"\n{passed}/{total} passed", end="")
    if failed: print(f", {failed} failed", end="")
    if errors: print(f", {errors} errors", end="")
    print()
    return 0 if failed == 0 and errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
