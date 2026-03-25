#!/usr/bin/env python3
"""Automated test suite for the MnM → ArnoldC interpreter generator.

Each test case defines a MnM program (source + sidecar), generates an ArnoldC
interpreter, compiles it, runs it, and checks the output against expected values.
"""

import json
import os
import subprocess
import sys
import tempfile

from generate_mnm_interpreter import generate

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JAR = os.path.join(BASE_DIR, "ArnoldC.jar")

# ── Test infrastructure ──────────────────────────────────────────────────────

def run_test(name, mnm_src, sidecar, expected_lines, timeout=10):
    """Generate, compile, run a MnM program and check output."""
    with tempfile.TemporaryDirectory() as tmp:
        arnoldc_path = os.path.join(tmp, "prog.arnoldc")
        generate(mnm_src, sidecar, output_path=arnoldc_path)

        # Compile (use relative filename so class name is simple)
        r = subprocess.run(
            ["java", "-jar", JAR, "prog.arnoldc"],
            capture_output=True, text=True, cwd=tmp, timeout=timeout,
        )
        if r.returncode != 0:
            return "COMPILE_FAIL", r.stderr.strip()

        # Run
        r = subprocess.run(
            ["java", "prog"],
            capture_output=True, text=True, cwd=tmp, timeout=timeout,
        )
        if r.returncode != 0:
            return "RUNTIME_FAIL", r.stderr.strip()

        actual = r.stdout.strip().split('\n') if r.stdout.strip() else []
        if actual == expected_lines:
            return "PASS", None
        else:
            return "FAIL", f"expected {expected_lines!r}, got {actual!r}"


def sidecar(strings=None, variables=None, int_inputs=None, str_inputs=None):
    """Convenience builder for sidecar dicts."""
    return {
        "strings": strings or [],
        "variables": variables or [],
        "inputs": {
            "int": int_inputs or [],
            "str": str_inputs or [],
        },
    }


# ── Test cases ───────────────────────────────────────────────────────────────

TESTS = []

def test(name, mnm_src, sidecar_data, expected):
    TESTS.append((name, mnm_src, sidecar_data, expected))


# 1. Hello world
test("hello_world",
     "OO Y\nOOOOOO\nBBBBBB\n",
     sidecar(strings=["Hello, world!"]),
     ["Hello, world!"])

# 2. Factorial(5) = 120
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

# 3. FizzBuzz 1–15
test("fizzbuzz",
     """N B
GG G
GG GG
YYYYYYYY
BBB BBBBBB
GG G
GG GGG
YYYYY
BB BB
GG G
GG GGGG
YYYYY
BB BBB
GG G
GG GGGGG
YYYYY
BB BBBB
GG G
O
B BBBBB
N BB
OO Y
B BBBBB
N BBB
OO YY
B BBBBB
N BBBB
OO YYY
N BBBBB
OOOOOO
GGGGGG G
B B
N BBBBBB
BBBBBB
""",
     sidecar(strings=["FizzBuzz", "Fizz", "Buzz"],
             variables=[1, 15, 15, 3, 5]),
     ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz",
      "11","Fizz","13","14","FizzBuzz"])

# 4. Just HALT (empty output)
test("halt_only",
     "BBBBBB\n",
     sidecar(),
     [])

# 5. Push and print
test("push_print",
     "G RRRRR\nO\nOOOOOO\nBBBBBB\n",     # PUSH 4, PRINT, NEWLINE, HALT
     sidecar(),
     ["4"])

# 6. Addition: 3 + 7 = 10
test("add",
     """G RRRR
G RRRRRRRR
Y
O
OOOOOO
BBBBBB
""",     # PUSH 3, PUSH 7, ADD, PRINT, NEWLINE, HALT
     sidecar(),
     ["10"])

# 7. Subtraction: 10 - 3 = 7
test("sub",
     """G RRRRRRRRRRR
G RRRR
YY
O
OOOOOO
BBBBBB
""",     # PUSH 10, PUSH 3, SUB, PRINT, NEWLINE, HALT
     sidecar(),
     ["7"])

# 8. Multiplication: 6 * 7 = 42
test("mul",
     """G RRRRRRR
G RRRRRRRR
YYY
O
OOOOOO
BBBBBB
""",     # PUSH 6, PUSH 7, MUL, PRINT, NEWLINE, HALT
     sidecar(),
     ["42"])

# 9. Division: 20 / 4 = 5
test("div",
     """G RRRRRRRRRRRRRRRRRRRRR
G RRRRR
YYYY
O
OOOOOO
BBBBBB
""",     # PUSH 20, PUSH 4, DIV, PRINT, NEWLINE, HALT
     sidecar(),
     ["5"])

# 10. Modulo: 17 % 5 = 2
test("mod",
     """G RRRRRRRRRRRRRRRRRR
G RRRRRR
YYYYY
O
OOOOOO
BBBBBB
""",     # PUSH 17, PUSH 5, MOD, PRINT, NEWLINE, HALT
     sidecar(),
     ["2"])

# 11. Equality: 5 == 5 → 1
test("eq_true",
     """G RRRRRR
G RRRRRR
YYYYYY
O
OOOOOO
BBBBBB
""",     # PUSH 5, PUSH 5, EQ, PRINT, NEWLINE, HALT
     sidecar(),
     ["1"])

# 12. Equality: 5 == 3 → 0
test("eq_false",
     """G RRRRRR
G RRRR
YYYYYY
O
OOOOOO
BBBBBB
""",
     sidecar(),
     ["0"])

# 13. GT: 7 > 3 → 1
test("gt_true",
     """G RRRRRRRR
G RRRR
YYYYYYYY
O
OOOOOO
BBBBBB
""",
     sidecar(),
     ["1"])

# 14. GT: 3 > 7 → 0
test("gt_false",
     """G RRRR
G RRRRRRRR
YYYYYYYY
O
OOOOOO
BBBBBB
""",
     sidecar(),
     ["0"])

# 15. LT: 3 < 7 → 1
test("lt_true",
     """G RRRR
G RRRRRRRR
YYYYYYY
O
OOOOOO
BBBBBB
""",
     sidecar(),
     ["1"])

# 16. LT: 7 < 3 → 0
test("lt_false",
     """G RRRRRRRR
G RRRR
YYYYYYY
O
OOOOOO
BBBBBB
""",
     sidecar(),
     ["0"])

# 17. NOT: NOT 0 → 1
test("not_zero",
     """G R
RRRRR
O
OOOOOO
BBBBBB
""",     # PUSH 0, NOT, PRINT, NEWLINE, HALT
     sidecar(),
     ["1"])

# 18. NOT: NOT 5 → 0
test("not_nonzero",
     """G RRRRRR
RRRRR
O
OOOOOO
BBBBBB
""",
     sidecar(),
     ["0"])

# 19. DUP: push 42, dup, print, print
test("dup",
     """G RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
GGGG
O
O
OOOOOO
BBBBBB
""",     # PUSH 42, DUP, PRINT, PRINT, NEWLINE, HALT
     sidecar(),
     ["42", "42"])

# 20. SWAP: push 1, push 2, swap → top=1, second=2
test("swap",
     """G RR
G RRR
R
O
O
OOOOOO
BBBBBB
""",     # PUSH 1, PUSH 2, SWAP, PRINT(1), PRINT(2), NEWLINE, HALT
     sidecar(),
     ["1", "2"])

# 21. Variables: LOAD/STORE
test("var_load_store",
     """G RRRRRR
GGG G
GG G
O
OOOOOO
BBBBBB
""",     # PUSH 5, STORE v0, LOAD v0, PRINT, NEWLINE, HALT
     sidecar(variables=[0]),
     ["5"])

# 22. INC/DEC
test("inc_dec",
     """GGGGGG G
GGGGGG G
GGGGGG G
GG G
O
GGGGGGG G
GG G
O
OOOOOO
BBBBBB
""",     # INC v0, INC v0, INC v0, LOAD v0, PRINT, DEC v0, LOAD v0, PRINT, NL, HALT
     sidecar(variables=[10]),
     ["13", "12"])

# 23. JMP: unconditional jump over a print
test("jmp",
     """B BBB
G RRRRRRRRRRR
O
N BBB
G RRRRRRRRRR
O
OOOOOO
BBBBBB
""",     # JMP label2, PUSH 10, PRINT, LABEL 2, PUSH 9, PRINT, NL, HALT
     sidecar(),
     ["9"])

# 24. JZ: jump when zero
test("jz_taken",
     """G R
BB BB
G RRRR
O
N BB
G RRR
O
OOOOOO
BBBBBB
""",     # PUSH 0, JZ label1, PUSH 3, PRINT, LABEL 1, PUSH 2, PRINT, NL, HALT
     sidecar(),
     ["2"])

# 25. JZ: no jump when non-zero
test("jz_not_taken",
     """G RR
BB BB
G RRRR
O
N BB
G RRR
O
OOOOOO
BBBBBB
""",     # PUSH 1, JZ label1, PUSH 3, PRINT, LABEL 1, PUSH 2, PRINT, NL, HALT
     sidecar(),
     ["3", "2"])

# 26. JNZ: jump when non-zero
test("jnz_taken",
     """G RR
BBB BB
G RRRR
O
N BB
G RRR
O
OOOOOO
BBBBBB
""",     # PUSH 1, JNZ label1, PUSH 3, PRINT, LABEL 1, PUSH 2, PRINT, NL, HALT
     sidecar(),
     ["2"])

# 27. JNZ: no jump when zero
test("jnz_not_taken",
     """G R
BBB BB
G RRRR
O
N BB
G RRR
O
OOOOOO
BBBBBB
""",     # PUSH 0, JNZ label1, PUSH 3, PRINT, LABEL 1, PUSH 2, PRINT, NL, HALT
     sidecar(),
     ["3", "2"])

# 28. AND: 1 AND 1 → 1
test("and_true",
     """G RR
G RR
RRR
O
OOOOOO
BBBBBB
""",
     sidecar(),
     ["1"])

# 29. AND: 1 AND 0 → 0
test("and_false",
     """G RR
G R
RRR
O
OOOOOO
BBBBBB
""",
     sidecar(),
     ["0"])

# 30. OR: 0 OR 1 → 1
test("or_true",
     """G R
G RR
RRRR
O
OOOOOO
BBBBBB
""",
     sidecar(),
     ["1"])

# 31. Count down loop: 3, 2, 1
test("countdown",
     """N B
GG G
GGGG
O
GGGGGGG G
GG G
G R
YYYYYYYY
BBB B
BBBBBB
""",     # LABEL 0, LOAD v0, DUP, PRINT, DEC v0, LOAD v0, PUSH 0, GT, JNZ label0, HALT
     sidecar(variables=[3]),
     ["3", "2", "1"])

# 32. Factorial(6) = 720
test("factorial_6",
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
     sidecar(variables=[0, 0], int_inputs=[[6]]),
     ["720"])

# 33. POP: push 1, push 2, pop, print → 1
test("pop",
     """G RR
G RRR
GGGGG
O
OOOOOO
BBBBBB
""",
     sidecar(),
     ["1"])

# 34. Multiple PRINT_STR
test("multi_print_str",
     """OO Y
OO YY
OO YYY
OOOOOO
BBBBBB
""",
     sidecar(strings=["Hello", "World", "!"]),
     ["Hello", "World", "!"])

# 35. ROT: push 1, 2, 3; rot → 2, 3, 1 (top=1)
test("rot",
     """G RR
G RRR
G RRRR
RR
O
O
O
OOOOOO
BBBBBB
""",     # PUSH 1, PUSH 2, PUSH 3, ROT, PRINT(top=1), PRINT(3), PRINT(2), NL, HALT
     sidecar(),
     ["1", "3", "2"])

# ── Runner ───────────────────────────────────────────────────────────────────

def main():
    passed = 0
    failed = 0
    errors = 0

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
            print(f"  ERROR {name} ({status}): {detail}")

    total = passed + failed + errors
    print(f"\n{passed}/{total} passed", end="")
    if failed:
        print(f", {failed} failed", end="")
    if errors:
        print(f", {errors} errors", end="")
    print()
    return 0 if failed == 0 and errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
