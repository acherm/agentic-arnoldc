#!/usr/bin/env python3
"""Benchmark: all BF execution paths compared.

Runs a set of BF programs through every available execution path and
reports timing. Compares:

  Path 0: Reference brainfuck interpreter (native C)
  Path 1: brainfuck.arnoldc (hardcoded BF, generated per program)
  Path 2: Compiler triple chain (generate_mnm_interpreter.py, static_fields)
  Path 3: bf_vm.arnoldc (direct stdin BF interpreter, fixed)
  Path 4: True triple chain (mnm_vm, reads MnM BF from stdin)

Usage:
    python3 benchmark_bf.py
    python3 benchmark_bf.py -k hello    # filter by name
"""

import json
import os
import subprocess
import sys
import tempfile
import time

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

from test_bf import TEST_SUITE, ENCODING
from generate_bf_interpreter import generate as generate_bf
from generate_mnm_bf import generate_mnm_bf
from generate_mnm_interpreter import generate as generate_mnm
from mnm_to_stdin import mnm_to_stdin

BRAINFUCK_REF = "/opt/homebrew/bin/brainfuck"
PATCHED_JAR = os.path.join(PROJECT_DIR, "ArnoldC-patched.jar")
ORIGINAL_JAR = os.path.join(PROJECT_DIR, "ArnoldC.jar")
TIMEOUT = 60

# Pre-compiled VMs (class dirs)
BF_VM_CLASS_DIR = PROJECT_DIR      # bf_vm.class
MNM_VM_CLASS_DIR = "/tmp"          # mnm_vm_test.class


def simulate_tape_size(bf_source):
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


def timed_run(cmd, input_data=None, cwd=None):
    """Run command, return (output_lines, elapsed_seconds) or (None, None) on error."""
    try:
        t0 = time.time()
        r = subprocess.run(cmd, input=input_data, capture_output=True, text=True,
                           timeout=TIMEOUT, cwd=cwd)
        elapsed = time.time() - t0
        if r.returncode != 0:
            return None, None
        out = [int(l.strip()) for l in r.stdout.strip().split('\n') if l.strip()] if r.stdout.strip() else []
        return out, elapsed
    except:
        return None, None


# ── Path 0: Reference BF interpreter ────────────────────────────────────

def run_path0(bf_source):
    if not bf_source.strip():
        return [], 0.0
    with tempfile.NamedTemporaryFile(mode='w', suffix='.b', delete=False) as f:
        f.write(bf_source); f.flush()
        try:
            t0 = time.time()
            r = subprocess.run([BRAINFUCK_REF, f.name], capture_output=True, timeout=TIMEOUT)
            elapsed = time.time() - t0
            return [b for b in r.stdout], elapsed
        except:
            return None, None
        finally:
            os.unlink(f.name)


# ── Path 1: brainfuck.arnoldc (hardcoded per program) ───────────────────

def run_path1(bf_source):
    bf_clean = ''.join(c for c in bf_source if c in ENCODING)
    if not bf_clean:
        return [], 0.0
    with tempfile.TemporaryDirectory() as tmp:
        arnoldc_path = os.path.join(tmp, "bf.arnoldc")
        generate_bf(bf_clean, output_path=arnoldc_path)
        r = subprocess.run(["java", "-jar", ORIGINAL_JAR, "bf.arnoldc"],
                           capture_output=True, text=True, cwd=tmp, timeout=TIMEOUT)
        if r.returncode != 0:
            return None, None
        # Run and time (output includes tape dump after "---")
        t0 = time.time()
        r = subprocess.run(["java", "bf"], capture_output=True, text=True,
                           cwd=tmp, timeout=TIMEOUT)
        elapsed = time.time() - t0
        if r.returncode != 0:
            return None, None
        lines = r.stdout.strip().split('\n')
        try:
            sep = lines.index('---')
            out = [int(l) for l in lines[:sep] if l.strip()]
        except ValueError:
            out = [int(l) for l in lines if l.strip() and l.strip().lstrip('-').isdigit()]
        return out, elapsed


# ── Path 2: Compiler triple chain ───────────────────────────────────────

def run_path2(bf_source):
    bf_clean = ''.join(c for c in bf_source if c in ENCODING)
    if not bf_clean:
        return [], 0.0
    tape_size = simulate_tape_size(bf_clean)
    mnm_src, sc, info = generate_mnm_bf(bf_clean, tape_size=tape_size)
    # Check if it fits (254-param limit)
    if info['num_vars'] + 1 > 254:
        return None, None  # too large for compiler approach
    with tempfile.TemporaryDirectory() as tmp:
        arnoldc_path = os.path.join(tmp, "prog.arnoldc")
        generate_mnm(mnm_src, sc, output_path=arnoldc_path, static_fields=True)
        r = subprocess.run(["java", "-jar", PATCHED_JAR, "prog.arnoldc"],
                           capture_output=True, text=True, cwd=tmp, timeout=TIMEOUT)
        if r.returncode != 0:
            return None, None
        return timed_run(["java", "prog"], cwd=tmp)


# ── Path 3: bf_vm.arnoldc (direct stdin) ────────────────────────────────

def run_path3(bf_source):
    bf_clean = ''.join(c for c in bf_source if c in ENCODING)
    if not bf_clean:
        return [], 0.0
    enc = {'>': 1, '<': 2, '+': 3, '-': 4, '.': 5, ',': 6, '[': 7, ']': 8}
    codes = [enc[c] for c in bf_clean]
    stdin_data = f"{len(codes)} " + " ".join(str(c) for c in codes) + "\n"
    return timed_run(["java", "-cp", BF_VM_CLASS_DIR, "bf_vm"],
                     input_data=stdin_data)


# ── Path 4: True triple chain (mnm_vm) ─────────────────────────────────

def run_path4(bf_source):
    bf_clean = ''.join(c for c in bf_source if c in ENCODING)
    if not bf_clean:
        return [], 0.0
    tape_size = simulate_tape_size(bf_clean)
    mnm_src, sc, info = generate_mnm_bf(bf_clean, tape_size=tape_size)
    vals = mnm_to_stdin(mnm_src, sc)
    stdin_data = '\n'.join(str(v) for v in vals) + '\n'
    return timed_run(["java", "-cp", MNM_VM_CLASS_DIR, "mnm_vm_test"],
                     input_data=stdin_data)


# ── Main ────────────────────────────────────────────────────────────────

# Select interesting subset for benchmarking (not all 38 — some are trivial)
BENCHMARK_CASES = [
    "empty_program", "single_inc_print", "multiply_3x2", "countdown_print",
    "nested_3x3x3", "print_A", "back_to_back_loops", "hello_world",
    "add_digits", "alphabet_ABC", "squares_1_to_5", "cell_copy",
    "print_ABCDEFG", "powers_of_2",
]

PATHS = [
    ("Path 0: ref bf",      run_path0),
    ("Path 1: arnoldc(hc)", run_path1),
    ("Path 2: compiler 3x", run_path2),
    ("Path 3: bf_vm",       run_path3),
    ("Path 4: true 3x",     run_path4),
]


def main():
    keyword = None
    for i, arg in enumerate(sys.argv):
        if arg == '-k' and i + 1 < len(sys.argv):
            keyword = sys.argv[i + 1]

    cases = [tc for tc in TEST_SUITE if tc.name in BENCHMARK_CASES]
    if keyword:
        cases = [tc for tc in TEST_SUITE if keyword.lower() in tc.name.lower()]

    # Header
    path_names = [name for name, _ in PATHS]
    print(f"{'Program':<25s} {'BF':>4s}", end="")
    for name in path_names:
        print(f"  {name:>17s}", end="")
    print()
    print("-" * (30 + 19 * len(PATHS)))

    for tc in cases:
        bf = tc.bf_source
        n = len([c for c in bf if c in ENCODING])
        print(f"{tc.name:<25s} {n:4d}", end="", flush=True)

        for path_name, path_fn in PATHS:
            out, elapsed = path_fn(bf)
            if elapsed is None:
                print(f"  {'—':>17s}", end="")
            elif elapsed < 0.001:
                print(f"  {'<0.001s':>17s}", end="")
            else:
                print(f"  {elapsed:>16.3f}s", end="")
            sys.stdout.flush()

        print()

    print()
    print("Legend:")
    print("  Path 0: Reference brainfuck interpreter (native C)")
    print("  Path 1: brainfuck.arnoldc — hardcoded BF program, original compiler")
    print("  Path 2: Compiler triple chain — Python-generated ArnoldC→MnM→BF")
    print("  Path 3: bf_vm.arnoldc — direct BF interpreter, reads BF from stdin")
    print("  Path 4: True triple chain — mnm_vm reads MnM BF interpreter from stdin")
    print("  — = not supported (program too large or compilation failed)")


if __name__ == "__main__":
    main()
