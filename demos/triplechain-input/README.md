# True Triple Chain with BF Input: ArnoldC → MnM → BF (`,`)

The hardest challenge: three interpreters deep, with **runtime input** flowing through all three levels. No Python at runtime.

```
User input        MnM BF interpreter       mnm_vm (ArnoldC)        Output
  6, 7    ──▶     1,129 MnM instr    ──▶   51,337 lines      ──▶   42
(BF , reads)      (in MnM input queue)     (pure ArnoldC)         (6 × 7)
```

## Quick Start

```bash
# Compile once:
java -jar ../../ArnoldC-patched.jar mnm_vm_multiply.arnoldc

# Multiply any two numbers — NO PYTHON:
./run.sh 6 7       # → 42
./run.sh 12 11     # → 132
./run.sh 3 14      # → 42
```

## How input flows through three interpreters

```
./run.sh 6 7
    │
    ▼
Shell script (no Python):
    cat stdin_base.txt     ← pre-computed MnM program + variables
    echo 2                 ← numInputs = 2
    echo 6                 ← first BF , will read this
    echo 7                 ← second BF , will read this
    │
    ▼  (piped to stdin)
mnm_vm_multiply (ArnoldC, 51,337 lines):
    Reads MnM program from stdin
    Loads input queue: iq[0]=6, iq[1]=7
    Executes MnM instructions...
    │
    ▼  (MnM READ_INT opcode)
MnM BF interpreter (1,129 instructions):
    Decodes BF: , > , < [ > [ > + > + << - ] >> [ << + >> - ] <<< - ] >> .
    BF , instruction → MnM READ_INT → reads from iq[] → value into BF tape
    First , reads 6, second , reads 7
    Loop computes 6 × 7 = 42
    BF . instruction → MnM PRINT → ArnoldC TALK TO THE HAND → stdout
    │
    ▼
Output: 42
```

## What's in this folder

| File | Lines | Description |
|------|------:|-------------|
| `mnm_vm_multiply.arnoldc` | 51,337 | ArnoldC MnM interpreter (fixed, reads from stdin) |
| `stdin_base.txt` | 2,304 | Pre-computed: MnM program + variable inits (no input queue) |
| `stdin_6x7.txt` | 2,307 | Complete stdin for 6×7 test (base + input queue [6, 7]) |
| `bf_multiply.mnm` | 1,129 | MnM BF interpreter source (with `,` support via READ_INT) |
| `run.sh` | — | Shell script: appends user input to base, pipes to ArnoldC |

## Why not chessboard?

The chessboard BF program (1,092 instructions) generates a MnM interpreter with 25,888 instructions and 1,148 variables. This requires ~53,000 ArnoldC static fields, which exceeds the **JVM constant pool limit** (65,535 entries). Each field needs ~3 constant pool entries (name + descriptor + reference), totaling ~160K entries.

This is a harder wall than the 100-variable, 64KB method, or Scanner limits we overcame earlier. It's baked into the JVM class file format (`u2 constant_pool_count`). The only solutions would be multi-class output (not supported by ArnoldC) or value packing.

| BF program | BF instr | MnM instr | MnM vars | ArnoldC fields | Constant pool | Fits? |
|-----------|------:|------:|-----:|------:|------:|:---:|
| multiply (this demo) | 33 | 1,129 | 44 | ~2,500 | ~7,500 | **Yes** |
| rot13 | 840 | 20,596 | 896 | ~42,000 | ~126,000 | No |
| chessboard | 1,092 | 25,888 | 1,148 | ~53,000 | ~160,000 | No |

## Regenerating

```bash
# Generate MnM BF interpreter (build-time Python, run once):
python3 ../../generate_mnm_bf.py  # creates bf_multiply.mnm + .json

# Build ArnoldC VM:
python3 ../../build_mnm_vm.py mnm_vm_multiply.arnoldc --prog 1200 --vars 50 --stack 30 --iq 10

# Compile:
java -jar ../../ArnoldC-patched.jar mnm_vm_multiply.arnoldc

# Run (no Python):
./run.sh 6 7
```
