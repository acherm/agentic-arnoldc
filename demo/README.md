# Demo: ArnoldC interprets MnM interprets Brainfuck

This folder contains all the intermediate artifacts for running esoteric language interpreters stacked three levels deep:

```
Brainfuck  ──▶  MnM Lang  ──▶  ArnoldC  ──▶  JVM  ──▶  output
 (12 instr)    (594 instr)    (12,411 lines)
```

A Brainfuck program (`+++[>++<-]>.`, which computes 3*2 and prints `6`) is interpreted by a MnM Lang program, which is itself interpreted by an ArnoldC program compiled to JVM bytecode.

## Prerequisites

- Java 8+
- [ArnoldC.jar](http://lhartikk.github.io/ArnoldC.jar) (in the parent directory)

## Quick Start

### The triple-interpreter chain (BF → MnM → ArnoldC)

```bash
# Compile the ArnoldC program (12,411 lines of Schwarzenegger quotes)
java -jar ../ArnoldC.jar mnm_bf_interpreter.arnoldc

# Run it — ArnoldC interprets MnM interpreting Brainfuck
java mnm_bf_interpreter
# Output: 6
```

That's it. One command compiles, one command runs three nested interpreters.

### Standalone MnM examples (MnM → ArnoldC)

```bash
# Hello World
java -jar ../ArnoldC.jar mnm_hello_world.arnoldc && java mnm_hello_world
# Output: Hello, world!

# Factorial(5)
java -jar ../ArnoldC.jar mnm_factorial.arnoldc && java mnm_factorial
# Output: 120

# FizzBuzz 1-15
java -jar ../ArnoldC.jar mnm_fizzbuzz.arnoldc && java mnm_fizzbuzz
# Output: 1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz
```

## What's in this folder

### Triple-interpreter chain (BF → MnM → ArnoldC)

| File | Lines | Description |
|------|------:|-------------|
| [`bf_program.txt`](bf_program.txt) | 1 | Brainfuck source: `+++[>++<-]>.` (computes 3×2, prints 6) |
| [`bf_interpreter.mnm`](bf_interpreter.mnm) | 594 | MnM Lang program that interprets the BF program above |
| [`bf_interpreter.mnm.json`](bf_interpreter.mnm.json) | — | MnM sidecar: 22 variables (BF opcodes in vars 6–17, tape in vars 18–21) |
| [`mnm_bf_interpreter.arnoldc`](mnm_bf_interpreter.arnoldc) | 12,411 | ArnoldC program that interprets the MnM interpreter above |

### Standalone MnM → ArnoldC examples

| MnM source | ArnoldC output | Lines | Description |
|------------|---------------|------:|-------------|
| [`hello_world.mnm`](hello_world.mnm) | [`mnm_hello_world.arnoldc`](mnm_hello_world.arnoldc) | 1,380 | Prints "Hello, world!" |
| [`factorial.mnm`](factorial.mnm) | [`mnm_factorial.arnoldc`](mnm_factorial.arnoldc) | 1,790 | Computes 5! = 120 |
| [`fizzbuzz.mnm`](fizzbuzz.mnm) | [`mnm_fizzbuzz.arnoldc`](mnm_fizzbuzz.arnoldc) | 2,063 | FizzBuzz 1–15 |

## Architecture

### How the triple chain works

```
                   generate_mnm_bf.py            generate_mnm_interpreter.py
                  ┌───────────────────┐          ┌───────────────────────────┐
  BF program      │  Encodes BF as    │   MnM    │  Encodes MnM as           │  ArnoldC
  +++[>++<-]>. ──▶│  MnM variables,   │──▶prog──▶│  ArnoldC if/else chains,  │──▶ program
  (12 instr)      │  generates MnM    │  (594    │  simulates stack+vars     │  (12,411
                  │  interpreter      │  instr)  │  with individual vars     │   lines)
                  └───────────────────┘          └───────────────────────────┘
```

**Step 1: BF → MnM** (`generate_mnm_bf.py`)

The BF program `+++[>++<-]>.` is encoded as integers (+=3, >=1, [=7, etc.) and stored in the MnM sidecar's variable array. A MnM BF interpreter is generated with:
- Variables 0–5: control state (ip, dp, prog\_len, depth, cur\_inst, cur\_val)
- Variables 6–17: BF program (12 encoded instructions)
- Variables 18–21: BF tape (4 cells)
- Comparison-chain dispatch for array access (MnM has no arrays either)

**Step 2: MnM → ArnoldC** (`generate_mnm_interpreter.py`)

The 594-instruction MnM program is compiled into ArnoldC:
- Instructions hardcoded in `fetchOpcode`/`fetchOperand` methods (594 if/else entries each)
- MnM's value stack simulated with 10 individual ArnoldC variables (`s0`–`s9`)
- MnM's 22 variables simulated with `v0`–`v21`
- Stack/variable access via `stackRead`/`condWrite` methods
- Each MnM opcode (PUSH, LOAD, STORE, EQ, JZ, INC, etc.) dispatched via sequential equality checks

**Step 3: ArnoldC → JVM** (`ArnoldC.jar`)

The 12,411-line ArnoldC file compiles to JVM bytecode. When executed, the main loop iterates through MnM instructions, which in turn iterate through BF instructions, producing `6`.

### The "no arrays" constraint

The entire architecture is shaped by one fundamental limitation: **none of the three languages have arrays**.

| Language | How it simulates arrays |
|----------|------------------------|
| Brainfuck | Has a tape (the one array-like structure) — that's the whole language |
| MnM Lang | Comparison chains: `if idx==0 load var0; if idx==1 load var1; ...` |
| ArnoldC | Same comparison chains, plus `condWrite(target, cell, old, new)` for writes |

At each interpreter level, "array access" becomes an if/else chain over individual variables. The triple chain stacks three levels of this simulation — the ArnoldC program contains if/else chains that dispatch MnM opcodes, which themselves contain if/else chains encoded as MnM instructions that dispatch BF opcodes and access the BF tape.

### Why generators instead of generic interpreters

A natural question: why not write one generic ArnoldC program that interprets any MnM program?

The answer is the no-arrays constraint. A generic interpreter would need:
1. **Dynamic program storage** — but ArnoldC can't store a variable-length instruction list
2. **Dynamic stack sizing** — but `stackRead(idx, s0, s1, ..., sN)` must have a fixed parameter count at compile time
3. **Dynamic string tables** — but `TALK TO THE HAND "..."` requires literal strings at compile time

A "bigger fixed-size" interpreter is theoretically possible (pre-allocate 200 instruction slots, 50 stack cells, etc.) but hits ArnoldC's **100-local-variable limit** — a hard constraint in ArnoldC's bytecode generator where more than 100 local variables per method causes compilation failure. The existing MnM BF interpreter from the [mnmlang repo](https://github.com/acherm/mnmlang) uses 150 variables and indeed cannot be compiled through ArnoldC.

The generator approach works around this by producing **tailored, compact programs** with exactly the resources needed. The BF program `+++[>++<-]>.` only needs 22 MnM variables and 10 ArnoldC stack cells — well within the 100-local budget.

### Size explosion across levels

| Level | Representation | Size |
|-------|---------------|------|
| Brainfuck | `+++[>++<-]>.` | 12 characters |
| MnM Lang | Comparison-chain interpreter | 594 lines |
| ArnoldC | Stack-machine interpreter | 12,411 lines |
| JVM bytecode | Compiled class file | ~74 KB |

Each level of interpretation adds roughly an order of magnitude in code size, driven by the if/else chains needed to simulate array indexing.

## Regenerating the artifacts

All files in this folder can be regenerated from scratch:

```bash
# Step 1: Generate MnM BF interpreter for the BF program
python3 ../generate_mnm_bf.py '+++[>++<-]>.'

# Step 2: Generate ArnoldC from MnM
python3 ../generate_mnm_interpreter.py bf_interpreter.mnm bf_interpreter.mnm.json mnm_bf_interpreter.arnoldc

# Step 3: Generate standalone MnM → ArnoldC examples
python3 ../generate_mnm_interpreter.py hello_world.mnm hello_world.mnm.json mnm_hello_world.arnoldc
python3 ../generate_mnm_interpreter.py factorial.mnm factorial.mnm.json mnm_factorial.arnoldc
python3 ../generate_mnm_interpreter.py fizzbuzz.mnm fizzbuzz.mnm.json mnm_fizzbuzz.arnoldc

# Or do the full chain in one shot:
python3 ../generate_mnm_bf.py '+++[>++<-]>.' --run
```

## Try your own BF program

```bash
# Any BF program that fits within ArnoldC's 100-variable budget
# (roughly: fewer than 50 BF instructions, fewer than 20 tape cells)

python3 ../generate_mnm_bf.py '+++++[>++++++<-]>.' --run
# Output: 30  (computes 5×6)

python3 ../generate_mnm_bf.py '+++++.>+++.' --run
# Output: 5 3  (two separate values)
```
