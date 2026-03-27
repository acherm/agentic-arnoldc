# Triple Chain: ArnoldC interprets MnM interprets Brainfuck

Three esoteric languages interpreting each other. A Brainfuck program runs inside a MnM interpreter, which runs inside an ArnoldC interpreter compiled to JVM bytecode.

This demo includes **two approaches** to the same triple chain — a compiler approach (faster, Python at build time) and a true interpreter approach (slower, no Python at runtime).

## Quick Start

### Prerequisites

- Java 8+
- `ArnoldC-patched.jar` (in the project root) — the patched compiler with static fields support

### Approach 1: Compiler (fast, Python-generated)

The MnM BF interpreter is compiled into a tailored ArnoldC program at build time. No stdin needed at runtime.

```bash
# BF Hello World — 55,747 lines of ArnoldC
java -jar ../../ArnoldC-patched.jar mnm_bf_helloworld.arnoldc
java mnm_bf_helloworld
# Output: 72 101 108 108 111 32 87 111 114 108 100 = "Hello World"
# Time: ~6.8 seconds

# Simple BF (3×2=6) — 12,593 lines of ArnoldC
java -jar ../../ArnoldC-patched.jar mnm_bf_interpreter.arnoldc
java mnm_bf_interpreter
# Output: 6
# Time: ~0.1 seconds
```

### Approach 2: True Interpreter (no Python at runtime)

A single fixed ArnoldC program (`mnm_vm_bf.arnoldc`, 26,757 lines) reads the MnM BF interpreter from stdin and executes it. The same ArnoldC file could run any MnM program.

```bash
# Compile the true interpreter (once):
java -jar ../../ArnoldC-patched.jar mnm_vm_bf.arnoldc

# Feed the MnM BF interpreter via stdin (staggered for ArnoldC's Scanner):
(while IFS= read -r line; do echo "$line"; sleep 0.08; done < bf_stdin_input.txt) | java mnm_vm_bf
# Output: 6
# Time: ~1m45s (97s stdin I/O + 7s execution)
```

## What's in this folder

### Compiler approach artifacts

| File | Lines | Description |
|------|------:|-------------|
| `bf_program.txt` | 1 | BF source: `+++[>++<-]>.` (computes 3×2) |
| `bf_interpreter.mnm` | 594 | MnM BF interpreter (22 variables) |
| `bf_interpreter.mnm.json` | — | MnM sidecar (BF program + tape in variables) |
| `mnm_bf_interpreter.arnoldc` | 12,593 | **Compiled** ArnoldC — tailored to this specific MnM program |
| | | |
| `bf_helloworld.txt` | 1 | BF Hello World (114 instructions) |
| `bf_helloworld_interpreter.mnm` | 2,883 | MnM BF interpreter for Hello World (127 variables) |
| `bf_helloworld_interpreter.mnm.json` | — | MnM sidecar |
| `mnm_bf_helloworld.arnoldc` | 55,747 | **Compiled** ArnoldC for Hello World |

### True interpreter artifacts

| File | Lines | Description |
|------|------:|-------------|
| `mnm_vm_bf.arnoldc` | 26,757 | **True interpreter** — fixed ArnoldC, reads any MnM from stdin |
| `bf_stdin_input.txt` | 1,213 | Stdin integer stream encoding the MnM BF interpreter |

## Architecture

### How three languages interpret each other

```
Level 3: Brainfuck         +++[>++<-]>.          12 characters
              │
              ▼ encoded as integers in MnM variables
Level 2: MnM Lang          594 instructions       BF interpreter with
                            22 variables           comparison-chain dispatch
              │
              ▼ (compiler approach)               ▼ (true interpreter)
Level 1: ArnoldC           12,593 lines            26,757 lines (fixed)
                            tailored per input      reads MnM from stdin
              │                                     │
              ▼                                     ▼
Level 0: JVM               bytecode                bytecode
              │                                     │
              ▼                                     ▼
         Output:            6                       6
```

### Compiler approach vs True interpreter

| | Compiler | True Interpreter |
|---|---|---|
| **ArnoldC file** | Different per MnM program | Always the same |
| **Python needed at runtime?** | No (build time only) | No |
| **MnM program delivery** | Hardcoded in ArnoldC | Read from stdin |
| **Build command** | `generate_mnm_interpreter.py` | `build_mnm_vm.py` (once) |
| **Performance** | Fast (data hardcoded) | Slow (stdin I/O + larger dispatch) |
| **Max MnM program** | ~4000 instructions | 600 (this build) |
| **Simple BF time** | 0.1s | 1m45s |
| **Hello World BF time** | 6.8s | Not tested (would need PROG≥2883) |

### Why the true interpreter is slow

Two compounding factors:

1. **Stdin I/O**: ArnoldC creates a new `Scanner(System.in)` per integer read. To prevent the Scanner from consuming buffered input, values must be delivered with `sleep 0.08` gaps. For 1,213 values, that's 97 seconds of waiting.

2. **Array access cost**: the true interpreter accesses program/stack/variables via if/else chains over static fields. Each `fetchOp(ip)` scans up to 600 entries. The compiler approach hardcodes data as constants, which the JVM can optimize better.

The actual interpretation (after stdin loading) takes only ~7 seconds — the same O(N) comparison-chain cost as the compiler approach.

### The "no arrays" constraint, three levels deep

None of the three languages have arrays. At each level, "array access" becomes a linear scan:

| Level | Array simulation technique |
|-------|--------------------------|
| **Brainfuck** | Has a tape — the one array-like structure (that's the whole language) |
| **MnM in BF interpreter** | Comparison chains: `if dp==0 load v18; if dp==1 load v19; ...` |
| **ArnoldC in MnM interpreter** | Same chains over static fields: `if idx==0 return s0; if idx==1 return s1; ...` |

The true interpreter stacks ALL of these: ArnoldC scans fields to simulate MnM's stack, which scans variables to simulate BF's tape, which scans the encoded program. Three nested linear scans per BF instruction.

## Regenerating the artifacts

```bash
# Compiler approach: BF → MnM → ArnoldC
python3 ../../generate_mnm_bf.py '+++[>++<-]>.'
python3 -c "
from generate_mnm_interpreter import generate; import json
with open('../../mnm_examples/bf_gen.mnm') as f: src=f.read()
with open('../../mnm_examples/bf_gen.mnm.json') as f: sc=json.load(f)
generate(src, sc, output_path='mnm_bf_interpreter.arnoldc', static_fields=True)
"

# True interpreter: build VM + generate stdin input
python3 ../../build_mnm_vm.py mnm_vm_bf.arnoldc --prog 600 --vars 30 --stack 30
python3 ../../mnm_to_stdin.py ../../mnm_examples/bf_gen.mnm ../../mnm_examples/bf_gen.mnm.json > bf_stdin_input.txt
```
