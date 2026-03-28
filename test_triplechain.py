#!/usr/bin/env python3
"""Test suite: BF programs through the true triple chain (ArnoldC → MnM → BF).

Runs each BF program through:
  1. Reference brainfuck interpreter → expected output
  2. generate_mnm_bf → mnm_to_stdin → mnm_vm (true interpreter) → actual output
  3. Compares outputs

Requires:
  - Reference brainfuck interpreter (brainfuck command)
  - Pre-compiled mnm_vm_test.class in /tmp/
  - Patched ArnoldC compiler

Usage:
    python3 test_triplechain.py           # run all tests
    python3 test_triplechain.py -v        # verbose
    python3 test_triplechain.py -k hello  # filter by name
"""

import os
import subprocess
import sys
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


def run_reference(bf_source):
    """Run BF through reference interpreter, return output as int list."""
    if not bf_source.strip():
        return []
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.b', delete=False) as f:
        f.write(bf_source)
        f.flush()
        try:
            r = subprocess.run(
                [BRAINFUCK_REF, f.name],
                capture_output=True, timeout=TIMEOUT,
            )
            return [b % 256 for b in r.stdout]
        finally:
            os.unlink(f.name)


def run_triple_chain(bf_source):
    """Run BF through ArnoldC → MnM → BF triple chain, return output as int list."""
    bf_clean = ''.join(c for c in bf_source if c in ENCODING)
    if not bf_clean:
        return []

    # Estimate tape size by simulation
    tape_size = simulate_tape_size(bf_clean)

    # Generate MnM BF interpreter
    mnm_src, sc, info = generate_mnm_bf(bf_clean, tape_size=tape_size)

    # Check if it fits in the VM
    import json
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mnm', delete=False) as mf:
        mf.write(mnm_src)
        mf.flush()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as jf:
            json.dump(sc, jf)
            jf.flush()
            try:
                vals = mnm_to_stdin(mnm_src, sc)
                stdin_data = '\n'.join(str(v) for v in vals) + '\n'

                r = subprocess.run(
                    ['java', '-cp', MNM_VM_CLASS_DIR, MNM_VM_CLASS],
                    input=stdin_data,
                    capture_output=True, text=True,
                    timeout=TIMEOUT,
                )
                if r.returncode != 0:
                    raise RuntimeError(f"Runtime error: {r.stderr[:100]}")

                output = []
                for line in r.stdout.strip().split('\n'):
                    line = line.strip()
                    if line:
                        output.append(int(line))
                return output
            finally:
                os.unlink(mf.name)
                os.unlink(jf.name)


def simulate_tape_size(bf_source):
    """Simulate BF execution to find actual max tape position."""
    pos = 0
    mx = 0
    ip = 0
    tape = {}
    bf = list(bf_source)
    steps = 0
    while ip < len(bf) and steps < 10_000_000:
        c = bf[ip]
        if c == '>':
            pos += 1
            mx = max(mx, pos)
        elif c == '<':
            pos -= 1
        elif c == '+':
            tape[pos] = tape.get(pos, 0) + 1
        elif c == '-':
            tape[pos] = tape.get(pos, 0) - 1
        elif c == '[':
            if tape.get(pos, 0) == 0:
                depth = 1
                while depth > 0:
                    ip += 1
                    if bf[ip] == '[': depth += 1
                    elif bf[ip] == ']': depth -= 1
        elif c == ']':
            if tape.get(pos, 0) != 0:
                depth = 1
                while depth > 0:
                    ip -= 1
                    if bf[ip] == ']': depth += 1
                    elif bf[ip] == '[': depth -= 1
                ip -= 1
        ip += 1
        steps += 1
    return max(mx + 2, 4)


def compare_outputs(reference, actual):
    """Compare reference (8-bit) and actual (32-bit) outputs.

    ArnoldC uses 32-bit integers, so values that rely on 8-bit wrapping
    may differ. We compare mod 256 for tolerance.
    """
    ref_mod = [v % 256 for v in reference]
    act_mod = [v % 256 for v in actual]
    return ref_mod == act_mod


def main():
    verbose = '-v' in sys.argv
    keyword = None
    for i, arg in enumerate(sys.argv):
        if arg == '-k' and i + 1 < len(sys.argv):
            keyword = sys.argv[i + 1]

    # Check prerequisites
    if not os.path.exists(os.path.join(MNM_VM_CLASS_DIR, f"{MNM_VM_CLASS}.class")):
        print(f"ERROR: {MNM_VM_CLASS}.class not found in {MNM_VM_CLASS_DIR}")
        print("Build it first:")
        print(f"  python3 build_mnm_vm.py /tmp/{MNM_VM_CLASS}.arnoldc --prog 3200 --vars 150 --stack 30")
        print(f"  java -jar ArnoldC-patched.jar /tmp/{MNM_VM_CLASS}.arnoldc")
        return 1

    passed = failed = errors = skipped = 0
    total_time = 0

    for tc in TEST_SUITE:
        if keyword and keyword.lower() not in tc.name.lower():
            continue
        if tc.skip:
            skipped += 1
            continue

        bf = tc.bf_source
        bf_clean = ''.join(c for c in bf if c in ENCODING)
        n_instr = len(bf_clean)

        try:
            # Reference
            ref_output = run_reference(bf)

            # Triple chain
            t0 = time.time()
            actual_output = run_triple_chain(bf)
            elapsed = time.time() - t0
            total_time += elapsed

            if compare_outputs(ref_output, actual_output):
                passed += 1
                marker = "PASS"
            else:
                failed += 1
                marker = "FAIL"

            if verbose or marker == "FAIL":
                print(f"  [{marker}] {tc.name:30s}  {n_instr:3d} BF  {elapsed:5.1f}s  ref={ref_output[:5]}{'...' if len(ref_output)>5 else ''} actual={actual_output[:5]}{'...' if len(actual_output)>5 else ''}")
            else:
                print(f"  [{marker}] {tc.name:30s}  {n_instr:3d} BF  {elapsed:5.1f}s")

        except Exception as e:
            errors += 1
            print(f"  [ERR ] {tc.name:30s}  {str(e)[:60]}")

    total = passed + failed + errors + skipped
    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed, {errors} errors, {skipped} skipped (of {total})")
    print(f"Total triple-chain time: {total_time:.1f}s")
    print(f"{'='*60}")
    return 0 if failed == 0 and errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
