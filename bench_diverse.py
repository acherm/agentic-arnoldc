#!/usr/bin/env python3
"""Diverse benchmark: bf_vm.arnoldc vs native brainfuck interpreter.

Tests multiple BF programs of varying size and complexity.
Measures both cold-JVM and warm-JVM (via BenchBfVm.java) times.
"""

import subprocess, time, json, os, sys, tempfile

# BF opcode encoding for bf_vm stdin protocol
ENC = {'>':1,'<':2,'+':3,'-':4,'.':5,',':6,'[':7,']':8}

def encode_bf(bf_src):
    """Convert BF source to bf_vm stdin integer protocol."""
    ops = [ENC[c] for c in bf_src if c in ENC]
    return f"{len(ops)} {' '.join(str(o) for o in ops)}"

# ── Test programs, ordered roughly by complexity ──────────────────────

PROGRAMS = {
    "trivial_print": {
        "bf": "++++++++++++++++++++++++++++++++++++++++++++++++.>+++++++++++++++++++++++++++++++++++++++++++++++++++.",
        "desc": "Print '01' (no loops)",
    },
    "multiply_3x2": {
        "bf": "+++[>++<-]>.",
        "desc": "3×2=6, single loop",
    },
    "countdown_5": {
        "bf": "+++++[.-]",
        "desc": "Print 5,4,3,2,1",
    },
    "nested_multiply": {
        "bf": "++[>+++[>++++<-]<-]>>.",
        "desc": "2×3×4=24, nested loops",
    },
    "hello_world": {
        "bf": "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.",
        "desc": "Classic Hello World",
    },
    "alphabet": {
        "bf": "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.+.+.+.+.+.+.+.+.+.+.+.+.+.+.+.+.+.+.+.+.+.+.+.+.+.",
        "desc": "Print A-Z",
    },
    "copy_cell": {
        "bf": "+++++++++++++++[>+>+<<-]>>[-<<+>>]<<.",
        "desc": "Copy cell value (35 iterations)",
    },
    "sierpinski": {
        "bf": "++++++++[>+>++++<<-]>++>>+<[-[>>+<<-]+>>]>+[-<<<[->[+[-]+>++>>>-<<]<[<]>>++++++[<<+++++>>-]+<<++.[-]<<]>.>+[>>]>+]",
        "desc": "Sierpinski triangle (32 rows)",
    },
    "squares": {
        "bf": "++++[>+++++<-]>[<+++++>-]+<+[>[>+>+<<-]++>>[<<+>>-]>>>[-]++>[-]+>>>+[[-]++++++>>>]<<<[[<++++++++<++>>-]+<.<[>----<-]<]<<[>>>>>[>>>[-]>>>[-]<<<<<<<<<<<<<<<<-]<<-]<<-]",
        "desc": "Print squares 0,1,4,9,...",
    },
    "bubble_sort_cells": {
        "bf": ">>++++[<++++[<++++>-]>-]<<[>+>+<<-]>>[<<+>>-]<[<[>>+>+<<<-]>>>[<<<+>>>-]<[->+<]<<-]>>[>+>+<<-]>>[<<+>>-]<[<[>>+>+<<<-]>>>[<<<+>>>-]<[->+<]<<-]>>[-]<<<[-]<<[-]>[>+<-]",
        "desc": "Cell manipulation / swap pattern",
    },
}

def bf_instruction_count(bf):
    return sum(1 for c in bf if c in ENC)

def run_reference(bf_src, runs=20):
    """Benchmark reference brainfuck interpreter."""
    with tempfile.NamedTemporaryFile(suffix='.bf', mode='w', delete=False) as f:
        f.write(bf_src)
        f.flush()
        fname = f.name

    times = []
    for _ in range(runs):
        try:
            t0 = time.perf_counter()
            r = subprocess.run(['brainfuck', fname], capture_output=True, timeout=10)
            t1 = time.perf_counter()
            times.append(t1 - t0)
        except subprocess.TimeoutExpired:
            os.unlink(fname)
            return None  # program too slow

    os.unlink(fname)
    return times

def run_bf_vm_cold(bf_src, runs=5):
    """Benchmark bf_vm with cold JVM (separate process each time)."""
    encoded = encode_bf(bf_src)
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        r = subprocess.run(['java', 'bf_vm'], input=encoded, capture_output=True, text=True, timeout=30)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return times

def run_bf_vm_warm(bf_src, warmup=10, runs=30):
    """Benchmark bf_vm with warm JVM using BenchBfVm harness."""
    encoded = encode_bf(bf_src)
    with tempfile.NamedTemporaryFile(suffix='.txt', mode='w', delete=False) as f:
        f.write(encoded)
        f.flush()
        fname = f.name

    r = subprocess.run(
        ['java', f'-Dwarmup={warmup}', f'-Druns={runs}', 'BenchBfVm', fname],
        capture_output=True, text=True, timeout=60
    )
    os.unlink(fname)

    # Parse output
    times = []
    for line in r.stdout.strip().split('\n'):
        if line.strip().startswith('run'):
            ms = float(line.split(':')[1].strip().replace(' ms', ''))
            times.append(ms)
    return times  # already in ms

def verify_outputs(bf_src):
    """Verify bf_vm output matches reference."""
    with tempfile.NamedTemporaryFile(suffix='.bf', mode='w', delete=False) as f:
        f.write(bf_src)
        f.flush()
        fname = f.name

    ref = subprocess.run(['brainfuck', fname], capture_output=True, timeout=30)
    os.unlink(fname)
    ref_values = list(ref.stdout)  # bytes

    encoded = encode_bf(bf_src)
    vm = subprocess.run(['java', 'bf_vm'], input=encoded, capture_output=True, text=True, timeout=30)
    vm_values = [int(x) % 256 for x in vm.stdout.strip().split('\n') if x.strip()]

    return ref_values == vm_values

def fmt_ms(ms):
    if ms < 0.01:
        return f"{ms*1000:.1f} µs"
    elif ms < 1:
        return f"{ms:.3f} ms"
    else:
        return f"{ms:.1f} ms"

def main():
    print("=" * 90)
    print("Diverse BF Benchmark: bf_vm.arnoldc vs native brainfuck interpreter")
    print("=" * 90)
    print()

    # Check BenchBfVm is compiled
    if not os.path.exists("BenchBfVm.class"):
        subprocess.run(['javac', 'BenchBfVm.java'], check=True)

    results = []

    for name, info in PROGRAMS.items():
        bf = info["bf"]
        n_ops = bf_instruction_count(bf)
        print(f"[{name}] {info['desc']} ({n_ops} ops)")

        # Verify correctness first
        ok = verify_outputs(bf)
        status = "✓" if ok else "✗ MISMATCH"
        print(f"  Correctness: {status}")
        if not ok:
            print("  SKIPPING (output mismatch)")
            continue

        # Reference interpreter
        ref_times = run_reference(bf, runs=20)
        if ref_times is None:
            print("  Reference interpreter timed out (>10s), skipping.")
            print()
            continue
        ref_avg = sum(ref_times) / len(ref_times) * 1000  # ms
        ref_min = min(ref_times) * 1000

        # bf_vm cold
        cold_times = run_bf_vm_cold(bf, runs=5)
        cold_avg = sum(cold_times) / len(cold_times) * 1000
        cold_min = min(cold_times) * 1000

        # bf_vm warm
        warm_times = run_bf_vm_warm(bf, warmup=10, runs=30)
        if warm_times:
            warm_avg = sum(warm_times) / len(warm_times)
            warm_min = min(warm_times)
        else:
            warm_avg = warm_min = float('nan')

        ratio_cold = cold_min / ref_min if ref_min > 0 else float('inf')
        ratio_warm = ref_min / warm_min if warm_min > 0 else float('inf')

        print(f"  Reference (native C):  avg={fmt_ms(ref_avg)}  min={fmt_ms(ref_min)}")
        print(f"  bf_vm (cold JVM):      avg={fmt_ms(cold_avg)}  min={fmt_ms(cold_min)}  ({ratio_cold:.0f}× slower)")
        print(f"  bf_vm (warm JVM/JIT):  avg={fmt_ms(warm_avg)}  min={fmt_ms(warm_min)}  ({ratio_warm:.1f}× faster)")
        print()

        results.append({
            "name": name,
            "desc": info["desc"],
            "ops": n_ops,
            "ref_min_ms": ref_min,
            "cold_min_ms": cold_min,
            "warm_min_ms": warm_min,
            "ratio_cold": ratio_cold,
            "ratio_warm": ratio_warm,
        })

    # Summary table
    print()
    print("=" * 90)
    print(f"{'Program':<22} {'Ops':>4} {'Native C':>10} {'Cold JVM':>10} {'Warm JIT':>10} {'Cold/Ref':>10} {'Ref/Warm':>10}")
    print("-" * 90)
    for r in results:
        print(f"{r['name']:<22} {r['ops']:>4} {fmt_ms(r['ref_min_ms']):>10} {fmt_ms(r['cold_min_ms']):>10} {fmt_ms(r['warm_min_ms']):>10} {r['ratio_cold']:>9.0f}× {r['ratio_warm']:>9.1f}×")
    print("-" * 90)
    print()
    print("Cold/Ref = how many times slower cold JVM is vs native C")
    print("Ref/Warm = how many times faster warm JIT is vs native C")

if __name__ == "__main__":
    main()
