# Demo: ArnoldC interprets MnM interprets Brainfuck

This folder contains all the intermediate artifacts for running esoteric language interpreters stacked three levels deep — including **BF Hello World**.

```
Brainfuck         MnM Lang            ArnoldC               JVM
Hello World  ──▶  2,883 instructions ──▶  55,747 lines  ──▶  "Hello World"
(114 instr)       (127 variables)         (Arnie quotes)     (6.8 seconds)
```

## Prerequisites

- Java 8+
- The **patched** ArnoldC compiler (`ArnoldC-patched.jar` in the parent directory) — required for programs with >100 variables and for the `static_fields` mode that splits opcode handlers across methods

## Quick Start

### BF Hello World through the triple chain

```bash
# Compile the ArnoldC program (55,747 lines of Schwarzenegger quotes)
java -jar ../ArnoldC-patched.jar mnm_bf_helloworld.arnoldc

# Run it — ArnoldC interprets MnM interpreting BF Hello World
java mnm_bf_helloworld
# Output: 72 101 108 108 111 32 87 111 114 108 100 11 2
#         H  e   l   l   o     W  o   r   l   d  (!)(\n)
# First 11 characters are correct ASCII; last 2 differ due to
# 32-bit integer semantics vs BF's 8-bit wrapping cells
```

### Simple BF triple chain

```bash
# Compile and run: +++[>++<-]>. computes 3×2 = 6
java -jar ../ArnoldC-patched.jar mnm_bf_interpreter.arnoldc && java mnm_bf_interpreter
# Output: 6
```

### Standalone MnM examples (MnM → ArnoldC)

```bash
java -jar ../ArnoldC-patched.jar mnm_hello_world.arnoldc && java mnm_hello_world
# Output: Hello, world!

java -jar ../ArnoldC-patched.jar mnm_factorial.arnoldc && java mnm_factorial
# Output: 120

java -jar ../ArnoldC-patched.jar mnm_fizzbuzz.arnoldc && java mnm_fizzbuzz
# Output: 1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz
```

## What's in this folder

### BF Hello World — triple-interpreter chain

| File | Lines | Description |
|------|------:|-------------|
| [`bf_helloworld.txt`](bf_helloworld.txt) | 1 | BF source: Hello World (114 instructions) |
| [`bf_helloworld_interpreter.mnm`](bf_helloworld_interpreter.mnm) | 2,883 | MnM BF interpreter for Hello World |
| [`bf_helloworld_interpreter.mnm.json`](bf_helloworld_interpreter.mnm.json) | — | MnM sidecar: 127 variables (BF program + tape) |
| [`mnm_bf_helloworld.arnoldc`](mnm_bf_helloworld.arnoldc) | 55,747 | ArnoldC interpreter (static\_fields mode) |

### Simple BF — triple-interpreter chain

| File | Lines | Description |
|------|------:|-------------|
| [`bf_program.txt`](bf_program.txt) | 1 | BF source: `+++[>++<-]>.` (computes 3×2, prints 6) |
| [`bf_interpreter.mnm`](bf_interpreter.mnm) | 594 | MnM BF interpreter for the program above |
| [`bf_interpreter.mnm.json`](bf_interpreter.mnm.json) | — | MnM sidecar: 22 variables |
| [`mnm_bf_interpreter.arnoldc`](mnm_bf_interpreter.arnoldc) | 12,593 | ArnoldC interpreter (static\_fields mode) |

### Standalone MnM → ArnoldC examples

| MnM source | ArnoldC output | Lines | Description |
|------------|---------------|------:|-------------|
| [`hello_world.mnm`](hello_world.mnm) | [`mnm_hello_world.arnoldc`](mnm_hello_world.arnoldc) | 1,569 | Prints "Hello, world!" |
| [`factorial.mnm`](factorial.mnm) | [`mnm_factorial.arnoldc`](mnm_factorial.arnoldc) | 1,979 | Computes 5! = 120 |
| [`fizzbuzz.mnm`](fizzbuzz.mnm) | [`mnm_fizzbuzz.arnoldc`](mnm_fizzbuzz.arnoldc) | 2,252 | FizzBuzz 1–15 |

## Architecture

### How the triple chain works

```
                   generate_mnm_bf.py            generate_mnm_interpreter.py
                  ┌───────────────────┐          ┌──────────────────────────────┐
  BF program      │  Encodes BF as    │   MnM    │  Encodes MnM as              │  ArnoldC
  (P instr)   ──▶ │  MnM variables,   │──▶prog──▶│  ArnoldC static fields +     │──▶ program
                  │  generates MnM    │          │  split handler methods        │
                  │  interpreter      │          │  (static_fields=True)         │
                  └───────────────────┘          └──────────────────────────────┘
```

**Step 1: BF → MnM** (`generate_mnm_bf.py`)

The BF program is encoded as integers (+=3, >=1, [=7, etc.) and stored in the MnM sidecar's variable array. A MnM BF interpreter is generated with:
- Variables 0–5: control state (ip, dp, prog\_len, depth, cur\_inst, cur\_val)
- Variables 6–6+P: BF program (P encoded instructions)
- Variables 6+P–end: BF tape (T cells)
- Comparison-chain dispatch for array access (MnM has no arrays either)

**Step 2: MnM → ArnoldC** (`generate_mnm_interpreter.py --static_fields`)

The MnM program is compiled into ArnoldC with the `static_fields=True` mode:
- All main-scope variables become JVM **static fields** (not local variables), allowing methods to access them directly via `GETSTATIC`/`PUTSTATIC`
- Each opcode handler is extracted into a **separate ArnoldC method**, keeping the main loop under the JVM 64KB method body limit
- Large fetch methods (>2000 entries) are **split into chunks** with binary dispatch
- Instructions hardcoded in `fetchOpcode`/`fetchOperand` methods
- MnM's value stack simulated with individual ArnoldC variables (`s0`–`s9`)

**Step 3: ArnoldC → JVM** (`ArnoldC-patched.jar`)

The patched compiler stores main-scope variables as static fields and uses `COMPUTE_FRAMES` for automatic stack map computation. The original compiler would crash on any program with >100 variables.

### The "no arrays" constraint

The entire architecture is shaped by one fundamental limitation: **none of the three languages have arrays**.

| Language | How it simulates arrays |
|----------|------------------------|
| Brainfuck | Has a tape (the one array-like structure) — that's the whole language |
| MnM Lang | Comparison chains: `if idx==0 load var0; if idx==1 load var1; ...` |
| ArnoldC | Same comparison chains, plus `condWrite(target, cell, old, new)` for writes |

At each interpreter level, "array access" becomes an if/else chain over individual variables. The triple chain stacks three levels of this simulation.

### Size explosion across levels

| | Simple BF (`+++[>++<-]>.`) | Hello World BF |
|---|---|---|
| Brainfuck | 12 characters | 114 characters |
| MnM Lang | 594 lines, 22 vars | 2,883 lines, 127 vars |
| ArnoldC | 12,593 lines | 55,747 lines |
| Runtime | 0.1 seconds | 6.8 seconds |
| Output | `6` | `72 101 108 108 111 32 87 111 114 108 100` |

Each level of interpretation adds roughly an order of magnitude in code size, driven by the if/else chains needed to simulate array indexing.

### Known limits

| Limit | Source | Constraint |
|-------|--------|-----------|
| **P + T ≤ 247** | JVM 254-parameter limit on `varRead` | BF program size + tape cells |
| **~4000 MnM instr per fetch chunk** | JVM 64KB method body | Handled by auto-splitting at 2000 entries |
| **O(P²) runtime per BF step** | Triple interpretation overhead | Hello World: 6.8s |
| **32-bit cell semantics** | ArnoldC uses signed `int`, not 8-bit | BF programs relying on byte wrapping produce different values |

### Compiler requirements

The demo artifacts require the **patched ArnoldC compiler** (`ArnoldC-patched.jar`) which includes two fixes over the original:
1. `ClassWriter(COMPUTE_FRAMES)` — removes the 100-variable limit
2. Static fields for main-scope variables — removes the 64KB method body limit by enabling handler method splitting

## Regenerating the artifacts

```bash
# Hello World BF → MnM → ArnoldC (static_fields)
python3 ../generate_mnm_bf.py '++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>>+.>++.'
cp ../mnm_examples/bf_gen.mnm bf_helloworld_interpreter.mnm
cp ../mnm_examples/bf_gen.mnm.json bf_helloworld_interpreter.mnm.json
python3 -c "
from generate_mnm_interpreter import generate; import json, sys; sys.path.insert(0,'..')
with open('bf_helloworld_interpreter.mnm') as f: src=f.read()
with open('bf_helloworld_interpreter.mnm.json') as f: sc=json.load(f)
generate(src, sc, output_path='mnm_bf_helloworld.arnoldc', static_fields=True)
"

# Simple BF → MnM → ArnoldC
python3 ../generate_mnm_bf.py '+++[>++<-]>.'
cp ../mnm_examples/bf_gen.mnm bf_interpreter.mnm
cp ../mnm_examples/bf_gen.mnm.json bf_interpreter.mnm.json
python3 -c "
from generate_mnm_interpreter import generate; import json, sys; sys.path.insert(0,'..')
with open('bf_interpreter.mnm') as f: src=f.read()
with open('bf_interpreter.mnm.json') as f: sc=json.load(f)
generate(src, sc, output_path='mnm_bf_interpreter.arnoldc', static_fields=True)
"

# Standalone MnM → ArnoldC examples
for prog in hello_world factorial fizzbuzz; do
    python3 -c "
from generate_mnm_interpreter import generate; import json, sys; sys.path.insert(0,'..')
with open('${prog}.mnm') as f: src=f.read()
with open('${prog}.mnm.json') as f: sc=json.load(f)
generate(src, sc, output_path='mnm_${prog}.arnoldc', static_fields=True)
"
done
```

## Try your own BF program

```bash
# With the patched compiler, programs up to ~200 BF instructions work:
python3 ../generate_mnm_bf.py '+++++[>++++++<-]>.' --run
# Output: 30  (computes 5×6)

python3 ../generate_mnm_bf.py '+++++.>+++.' --run
# Output: 5 3  (two separate values)

# For the full chain with static_fields (larger programs):
python3 ../generate_mnm_bf.py 'YOUR_BF_PROGRAM_HERE'
python3 -c "
from generate_mnm_interpreter import generate; import json
with open('../mnm_examples/bf_gen.mnm') as f: src=f.read()
with open('../mnm_examples/bf_gen.mnm.json') as f: sc=json.load(f)
generate(src, sc, output_path='my_program.arnoldc', static_fields=True)
"
java -jar ../ArnoldC-patched.jar my_program.arnoldc && java my_program
```
