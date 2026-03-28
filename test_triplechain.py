#!/usr/bin/env python3
"""Test suite: BF programs through the true triple chain (ArnoldC → MnM → BF).

Mirrors test_bf.py's structure but runs BF programs through three interpreters:

  For each BF program:
    1. Python (preparation): generate_mnm_bf → mnm_to_stdin → stdin integers
    2. Java  (pure ArnoldC): cat stdin | java mnm_vm     ← this is the test
    3. Compare: triple chain output vs reference brainfuck interpreter

The Java execution in step 2 is pure ArnoldC — a single fixed program
(mnm_vm) reads MnM instructions from stdin, which interpret BF opcodes.
No Python in the execution loop.

Requires:
  - Reference brainfuck interpreter (/opt/homebrew/bin/brainfuck)
  - Pre-compiled mnm_vm_test.class in /tmp/
    Build: python3 build_mnm_vm.py /tmp/mnm_vm_test.arnoldc --prog 3200 --vars 150 --stack 30
           java -jar ArnoldC-patched.jar /tmp/mnm_vm_test.arnoldc

Usage:
    python3 test_triplechain.py           # run all 38 tests
    python3 test_triplechain.py -v        # verbose (show decoded output)
    python3 test_triplechain.py -k hello  # filter by name
"""

import json
import os
import subprocess
import sys
import tempfile
import time

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BRAINFUCK_REF = "/opt/homebrew/bin/brainfuck"
MNM_VM_CLASS_DIR = "/tmp"
MNM_VM_CLASS = "mnm_vm_test"
TIMEOUT = 30

sys.path.insert(0, PROJECT_DIR)
from test_bf import TEST_SUITE, ENCODING
from generate_mnm_bf import generate_mnm_bf
from mnm_to_stdin import mnm_to_stdin


# ── BF tape simulation (for accurate tape sizing) ───────────────────────

def simulate_tape_size(bf_source):
    """Simulate BF execution to find actual max tape position."""
    pos = mx = ip = 0
    tape = {}
    bf = list(bf_source)
    steps = 0
    while ip < len(bf) and steps < 10_000_000:
        c = bf[ip]
        if c == '>': pos += 1; mx = max(mx, pos)
        elif c == '<': pos -= 1
        elif c == '+': tape[pos] = tape.get(pos, 0) + 1
        elif c == '-': tape[pos] = tape.get(pos, 0) - 1
        elif c == '[':
            if tape.get(pos, 0) == 0:
                d = 1
                while d > 0:
                    ip += 1; d += 1 if bf[ip] == '[' else (-1 if bf[ip] == ']' else 0)
        elif c == ']':
            if tape.get(pos, 0) != 0:
                d = 1
                while d > 0:
                    ip -= 1; d += 1 if bf[ip] == ']' else (-1 if bf[ip] == '[' else 0)
                ip -= 1
        ip += 1; steps += 1
    return max(mx + 2, 4)


# ── Reference interpreter ───────────────────────────────────────────────

def run_reference(bf_source):
    """Run BF through reference interpreter, return output as int list."""
    if not bf_source.strip():
        return []
    with tempfile.NamedTemporaryFile(mode='w', suffix='.b', delete=False) as f:
        f.write(bf_source)
        f.flush()
        try:
            r = subprocess.run([BRAINFUCK_REF, f.name],
                               capture_output=True, timeout=TIMEOUT)
            return [b % 256 for b in r.stdout]
        finally:
            os.unlink(f.name)


# ── Triple chain execution ──────────────────────────────────────────────

def run_triple_chain(bf_source):
    """Run BF through ArnoldC → MnM → BF triple chain.

    Steps:
      1. (Python) Encode BF as MnM BF interpreter
      2. (Python) Convert MnM to stdin integer stream
      3. (Java/ArnoldC) Feed stdin to mnm_vm → output
    """
    bf_clean = ''.join(c for c in bf_source if c in ENCODING)
    if not bf_clean:
        return [], 0.0

    tape_size = simulate_tape_size(bf_clean)
    mnm_src, sc, info = generate_mnm_bf(bf_clean, tape_size=tape_size)
    vals = mnm_to_stdin(mnm_src, sc)
    stdin_data = '\n'.join(str(v) for v in vals) + '\n'

    # ── This is the pure ArnoldC execution ──
    t0 = time.time()
    r = subprocess.run(
        ['java', '-cp', MNM_VM_CLASS_DIR, MNM_VM_CLASS],
        input=stdin_data,
        capture_output=True, text=True,
        timeout=TIMEOUT,
    )
    elapsed = time.time() - t0

    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:100])

    output = []
    for line in r.stdout.strip().split('\n'):
        line = line.strip()
        if line:
            output.append(int(line))

    return output, elapsed


# ── Test runner ─────────────────────────────────────────────────────────

def main():
    verbose = '-v' in sys.argv
    keyword = None
    for i, arg in enumerate(sys.argv):
        if arg == '-k' and i + 1 < len(sys.argv):
            keyword = sys.argv[i + 1]

    if not os.path.exists(os.path.join(MNM_VM_CLASS_DIR, f"{MNM_VM_CLASS}.class")):
        print(f"ERROR: {MNM_VM_CLASS}.class not found in {MNM_VM_CLASS_DIR}")
        print("Build it:")
        print(f"  python3 build_mnm_vm.py /tmp/{MNM_VM_CLASS}.arnoldc --prog 3200 --vars 150 --stack 30")
        print(f"  java -jar ArnoldC-patched.jar /tmp/{MNM_VM_CLASS}.arnoldc")
        return 1

    cases = TEST_SUITE
    if keyword:
        cases = [tc for tc in cases if keyword.lower() in tc.name.lower()]

    print("=" * 70)
    print(f"Triple Chain Test Suite: ArnoldC → MnM → BF ({len(cases)} tests)")
    print("  Reference: brainfuck interpreter")
    print(f"  Under test: java {MNM_VM_CLASS} (pure ArnoldC, reads MnM from stdin)")
    print("=" * 70)
    print()

    passed = failed = errors = skipped = 0
    total_arnoldc_time = 0

    for tc in cases:
        if tc.skip:
            skipped += 1
            print(f"  \033[33m[SKIP]\033[0m {tc.name:<30s}  {tc.skip}")
            continue

        bf = tc.bf_source
        n = len([c for c in bf if c in ENCODING])

        try:
            ref_output = run_reference(bf)
            actual_output, arnoldc_time = run_triple_chain(bf)
            total_arnoldc_time += arnoldc_time

            # Compare mod 256 (ArnoldC uses 32-bit ints, BF uses 8-bit cells)
            ref_mod = [v % 256 for v in ref_output]
            act_mod = [v % 256 for v in actual_output]

            if ref_mod == act_mod:
                passed += 1
                print(f"  \033[32m[PASS]\033[0m {tc.name:<30s}  {n:3d} BF  ({arnoldc_time:.2f}s)")
                if verbose and actual_output:
                    chars = ''.join(chr(v % 256) if 32 <= (v % 256) < 127 else '.' for v in actual_output)
                    print(f"         output: {actual_output[:8]}{'...' if len(actual_output) > 8 else ''} = \"{chars}\"")
            else:
                failed += 1
                print(f"  \033[31m[FAIL]\033[0m {tc.name:<30s}  {n:3d} BF  ({arnoldc_time:.2f}s)")
                print(f"         ref={ref_mod[:5]}  actual={act_mod[:5]}")

        except subprocess.TimeoutExpired:
            errors += 1
            print(f"  \033[31m[ERR ]\033[0m {tc.name:<30s}  Timeout ({TIMEOUT}s)")
        except Exception as e:
            errors += 1
            print(f"  \033[31m[ERR ]\033[0m {tc.name:<30s}  {str(e)[:60]}")

    total = passed + failed + errors + skipped
    print()
    print("=" * 70)
    color = "\033[32m" if failed == 0 and errors == 0 else "\033[31m"
    print(f"{color}Results: {passed} passed, {failed} failed, {errors} errors, {skipped} skipped\033[0m")
    print(f"ArnoldC execution time: {total_arnoldc_time:.1f}s (pure ArnoldC, no Python)")
    print(f"Total wall time includes Python preparation (generate MnM + encode stdin)")
    print("=" * 70)
    return 0 if failed == 0 and errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
