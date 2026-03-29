# Agentic ArnoldC

25 programming challenges, a Brainfuck interpreter, an MnM Lang interpreter, a triple-interpreter chain (ArnoldC→MnM→BF), compiler patches, and automated test suites -- all in **[ArnoldC](https://github.com/lhartikk/ArnoldC)**, the esoteric programming language where every keyword is an Arnold Schwarzenegger movie quote.

Everything was written, compiled, debugged, and verified by AI agents (Claude) in a single conversation.

> `IT'S SHOWTIME` = begin program. `YOU HAVE BEEN TERMINATED` = end program. `TALK TO THE HAND` = print. You get the idea.

## What is ArnoldC?

ArnoldC is an imperative programming language that compiles to JVM bytecode. Its entire syntax is composed of Schwarzenegger one-liners:

| ArnoldC | Meaning |
|---------|---------|
| `IT'S SHOWTIME` | Begin main |
| `YOU HAVE BEEN TERMINATED` | End main |
| `HEY CHRISTMAS TREE x` | Declare variable x |
| `YOU SET US UP 0` | Initialize to 0 |
| `GET TO THE CHOPPER x` | Begin assignment to x |
| `HERE IS MY INVITATION y` | Set value to y |
| `GET UP z` | Add z |
| `GET DOWN z` | Subtract z |
| `YOU'RE FIRED z` | Multiply by z |
| `HE HAD TO SPLIT z` | Divide by z |
| `I LET HIM GO z` | Modulo z |
| `LET OFF SOME STEAM BENNET z` | Greater than z |
| `YOU ARE NOT YOU YOU ARE ME z` | Equals z |
| `ENOUGH TALK` | End assignment |
| `TALK TO THE HAND x` | Print x |
| `BECAUSE I'M GOING TO SAY PLEASE x` | If x |
| `BULLSHIT` | Else |
| `YOU HAVE NO RESPECT FOR LOGIC` | End if |
| `STICK AROUND x` | While x |
| `CHILL` | End while |
| `LISTEN TO ME VERY CAREFULLY f` | Declare method f |
| `I'LL BE BACK x` | Return x |
| `HASTA LA VISTA, BABY` | End method |
| `DO IT NOW f` | Call method f |

## Repository Contents

```
.
├── challenges/
│   └── challenge01.arnoldc .. challenge25.arnoldc   # 25 programming challenges
├── brainfuck.arnoldc                                # BF interpreter (hardcoded program)
├── bf_vm.arnoldc                                    # BF interpreter (reads any BF from stdin)
├── build_bf_vm.py                                   # Generates bf_vm.arnoldc (run once)
├── BenchBfVm.java                                   # JIT benchmark harness for bf_vm
├── bench_diverse.py                                 # Diverse benchmark: bf_vm vs native C
├── generate_bf_interpreter.py                       # Python generator for BF interpreter
├── test_bf.py                                       # Automated test suite (38 BF tests)
├── mnm_vm.arnoldc                                   # True MnM interpreter (fixed, reads from stdin)
├── build_mnm_vm.py                                  # Generates mnm_vm.arnoldc (run once)
├── mnm_to_stdin.py                                  # Converts .mnm+.json to stdin integer stream
├── test_mnm_vm.py                                   # Test suite for true interpreter (16 tests)
├── generate_mnm_interpreter.py                      # MnM→ArnoldC compiler (alternative approach)
├── generate_mnm_bf.py                               # BF→MnM→ArnoldC triple-chain generator
├── test_mnm.py                                      # Test suite for compiler approach (35 tests)
├── mnm_examples/                                    # MnM Lang example programs
│   ├── hello_world.mnm / .mnm.json
│   ├── factorial.mnm / .mnm.json
│   └── fizzbuzz.mnm / .mnm.json
├── ArnoldC-patched.jar                              # Patched compiler (variable + method limits removed)
├── demos/                                           # Pre-built artifacts for all interpreter chains
│   ├── triplechain/                                 # ArnoldC → MnM → BF (compiler + true interpreter)
│   ├── mnm-standalone/                              # MnM programs with true interpreter
│   └── mnm-compiler/                                # MnM programs compiled to ArnoldC
└── README.md
```

## The 25 Challenges

### Easy (1-10)

| # | Challenge | File | Description | Example |
|---|-----------|------|-------------|---------|
| 1 | Sum 1 to N | [`challenge01.arnoldc`](challenges/challenge01.arnoldc) | Read n, print 1+2+...+n | 5 &rarr; 15 |
| 2 | Countdown | [`challenge02.arnoldc`](challenges/challenge02.arnoldc) | Print n down to 0 | 4 &rarr; 4,3,2,1,0 |
| 3 | Even or Odd | [`challenge03.arnoldc`](challenges/challenge03.arnoldc) | Print EVEN or ODD | 7 &rarr; ODD |
| 4 | Max of Two | [`challenge04.arnoldc`](challenges/challenge04.arnoldc) | Print the larger of two integers | 12,9 &rarr; 12 |
| 5 | Absolute Value | [`challenge05.arnoldc`](challenges/challenge05.arnoldc) | Print \|n\| | -8 &rarr; 8 |
| 6 | Multiplication Table | [`challenge06.arnoldc`](challenges/challenge06.arnoldc) | Print n*1 through n*10 | 3 &rarr; 3,6,...,30 |
| 7 | Power of Two | [`challenge07.arnoldc`](challenges/challenge07.arnoldc) | Print 2^0 through 2^n | 4 &rarr; 1,2,4,8,16 |
| 8 | Multiply w/o `*` | [`challenge08.arnoldc`](challenges/challenge08.arnoldc) | Repeated addition only | 4,3 &rarr; 12 |
| 9 | Integer Average | [`challenge09.arnoldc`](challenges/challenge09.arnoldc) | Print (a+b)/2 | 7,10 &rarr; 8 |
| 10 | Sum of Digits | [`challenge10.arnoldc`](challenges/challenge10.arnoldc) | Sum decimal digits | 527 &rarr; 14 |

### Easy/Medium -- Original (11-20)

| # | Challenge | File | Description | Example |
|---|-----------|------|-------------|---------|
| 11 | Total Counter | [`challenge11.arnoldc`](challenges/challenge11.arnoldc) | Sum of 6 integers | 3,4,2,5,1,6 &rarr; 21 |
| 12 | Largest Category | [`challenge12.arnoldc`](challenges/challenge12.arnoldc) | Find label (A-F) with highest count | 3,9,2,5,1,6 &rarr; B |
| 13 | Vending Machine | [`challenge13.arnoldc`](challenges/challenge13.arnoldc) | Greedy coin change | 68 &rarr; 2Q,1D,1N,3P |
| 14 | Staircase | [`challenge14.arnoldc`](challenges/challenge14.arnoldc) | Print staircase pattern | 4 &rarr; 1,11,111,1111 |
| 15 | String Length | [`challenge15.arnoldc`](challenges/challenge15.arnoldc) | Count integers until sentinel 0 | 9 codes + 0 &rarr; 9 |
| 16 | Repeat Phrase | [`challenge16.arnoldc`](challenges/challenge16.arnoldc) | Print HELLO k times | 3 &rarr; HELLO x3 |
| 17 | Palindrome | [`challenge17.arnoldc`](challenges/challenge17.arnoldc) | Check if number is palindrome | 1221 &rarr; YES |
| 18 | Collatz Steps | [`challenge18.arnoldc`](challenges/challenge18.arnoldc) | Count Collatz steps to 1 | 6 &rarr; 8 |
| 19 | Run-Length Decode | [`challenge19.arnoldc`](challenges/challenge19.arnoldc) | Expand (count,value) pairs | 3,65,2,66 &rarr; 65x3,66x2 |
| 20 | Mini Gradebook | [`challenge20.arnoldc`](challenges/challenge20.arnoldc) | Min, max, average of 5 grades | 12,8,15,10,14 &rarr; 8,15,11 |

### Hard + Bonus (21-25)

| # | Challenge | File | Description | Example |
|---|-----------|------|-------------|---------|
| 21 | Recursive Fibonacci | [`challenge21.arnoldc`](challenges/challenge21.arnoldc) | fib(n) via recursive method | 7 &rarr; 13 |
| 22 | Tiny Virtual Machine | [`challenge22.arnoldc`](challenges/challenge22.arnoldc) | Interpreter for PUSH/ADD/SUB/MUL/PRINT/HALT | PUSH 5, PRINT &rarr; 5 |
| 23 | Text Histogram | [`challenge23.arnoldc`](challenges/challenge23.arnoldc) | Bar chart for 6 labeled counts | 2,4,1,... &rarr; A:2, B:4,... |
| 24 | Digital Clock Tick | [`challenge24.arnoldc`](challenges/challenge24.arnoldc) | Advance time by one second | 23:59:59 &rarr; 0:0:0 |
| 25 | Caesar Cipher | [`challenge25.arnoldc`](challenges/challenge25.arnoldc) | Shift ASCII codes by k | shift 3, CODE &rarr; FRGH |

**25/25 PASS** -- all compiled and verified with the actual ArnoldC compiler.

## Capstone: Brainfuck Interpreter in ArnoldC

[`brainfuck.arnoldc`](brainfuck.arnoldc) is an ArnoldC program that **interprets and executes Brainfuck programs**. It simulates an entire programming language inside an esoteric language that has no arrays, no strings, and only `println` for output.

### Architecture

The interpreter faces a fundamental problem: ArnoldC has no arrays. The solution uses **individual variables as simulated arrays** with method-based dispatch:

| Component | Implementation |
|-----------|---------------|
| Memory tape | Individual cell variables (`c0`-`cN`), accessed via `tapeRead`/`tapeWrite` methods |
| BF program | **Hardcoded constants** in the `fetch` method body (avoids ArnoldC's 100-local-variable limit) |
| Data pointer | Single variable `dp` |
| Instruction pointer | Single variable `ip` |
| Bracket matching | Runtime depth-counting scan using the `fetch` method |

Three methods simulate array access:
- `fetch(idx)` -- returns the instruction at position `idx`; instructions are hardcoded as constants in the if/else chain, so program size is effectively unlimited
- `tapeRead(idx, c0, c1, ..., cN)` -- returns the cell value at position `idx` via parameter passing
- `tapeWrite(targetIdx, cellIdx, oldVal, newVal)` -- returns `newVal` if indices match, `oldVal` otherwise

### BF Instruction Encoding

| BF | Code | BF | Code |
|----|------|----|------|
| `>` | 1 | `.` | 5 |
| `<` | 2 | `,` | 6 |
| `+` | 3 | `[` | 7 |
| `-` | 4 | `]` | 8 |
| (end) | 0 | | |

### Execution Model

- **Tape:** Auto-sized per program, unbounded integers, initialized to 0
- **Program size:** Effectively unlimited (instructions are hardcoded constants, not variables)
- **Output:** Numeric (prints cell value as integer)
- **Brackets:** Matched at runtime via forward/backward scanning with nesting depth tracking
- **Input (`,`):** Not supported
- **Post-execution:** Dumps full tape state and data pointer for verification

### How to Use

```bash
# Use the generator (auto-sizes tape and program):
python3 -c "
from generate_bf_interpreter import generate
generate('+++++.', output_path='my_program.arnoldc')
"
java -jar ArnoldC.jar my_program.arnoldc
java my_program

# Hello World:
python3 -c "
from generate_bf_interpreter import generate
hw = '++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.'
generate(hw, output_path='hello.arnoldc')
"
java -jar ArnoldC.jar hello.arnoldc && java hello
# Output: 72 101 108 108 111 32 87 111 114 108 100 33 10  (= "Hello World!\n")
```

### Why This Is Hard

This program doesn't just solve a computation -- it **simulates another programming language**. In a language with no arrays, no strings, no random access, and no `print` without newline, it:

- Manually represents and updates a memory tape via individual variables
- Hardcodes BF instructions as constants in a method's if/else chain
- Dispatches 7 instruction types via sequential equality checks
- Implements nested bracket matching with depth-counting forward/backward scans
- Uses a 4-parameter `tapeWrite` method called N times per write to conditionally update exactly one cell

The result: **a working, tested interpreter for a Turing-complete language, written entirely in Arnold Schwarzenegger quotes.**

## MnM Lang Interpreter in ArnoldC

[MnM Lang](https://github.com/mufeedvh/mnmlang) is an esoteric programming language where source code is a grid of colored M&M candies. It's a stack-based VM with 37 opcodes across 6 color families. Programs come with a `.mnm.json` sidecar file containing strings, variables, and input queues.

A Python generator ([`generate_mnm_interpreter.py`](generate_mnm_interpreter.py)) takes a `.mnm` program + sidecar and produces a tailored ArnoldC file that executes it. Unlike the Brainfuck interpreter (which is a single fixed ArnoldC program), this is a **compiler** rather than an interpreter — the generated ArnoldC varies in shape depending on the input program's resource requirements. See [Architecture Limitation](#architecture-limitation-compiler-vs-interpreter) for why, and the roadmap toward a true single-file interpreter.

### Why a Generator, Not a Single Generic Interpreter?

A natural question: why generate a *specific* ArnoldC program per MnM input, rather than writing one *generic* ArnoldC interpreter that reads any MnM program?

The answer is **ArnoldC has no arrays**. This forces three things to be known at generation time:

1. **The program itself** — MnM instructions are stored via `fetchOpcode(idx)` / `fetchOperand(idx)` methods that are giant if/else chains matching each index to a hardcoded constant. There's no way to store a list of instructions and index into it at runtime.

2. **Stack and variable sizes** — `stackRead(idx, s0, s1, ..., sN)` passes every cell as a parameter and uses if/else to select the right one. The number of parameters must be fixed at compile time.

3. **String literals** — `printStr(idx)` has each string baked into a `TALK TO THE HAND "..."` inside an if/else chain. ArnoldC has no string variables.

A "more generic" approach would mean pre-allocating huge fixed-size arrays (200 instruction slots, 50 stack cells, etc.) and reading the program from stdin. But this would produce enormous if/else chains (~3000+ lines just for fetch methods), stdin input would require reading hundreds of integers one at a time, and strings would remain impossible to pass dynamically. It would still not be truly generic — just a bigger fixed-size interpreter.

The generator approach is the pragmatic sweet spot: it produces a **compact, tailored interpreter** for each MnM program, with exactly the resources needed.

### Architecture

| Component | Implementation |
|-----------|---------------|
| Value stack | Individual variables (`s0`–`sN`), accessed via `stackRead` / `condWrite` |
| MnM variables | Individual variables (`v0`–`vK`), initialized from sidecar, accessed via `varRead` / `condWrite` |
| Call stack | Individual variables (`cs0`–`csM`) for CALL/RET subroutines |
| MnM program | Hardcoded constants in `fetchOpcode` / `fetchOperand` methods |
| Input queues | Pre-loaded from sidecar JSON, accessed via `readIntVal` method |
| Strings | Hardcoded `TALK TO THE HAND "..."` in `printStr` method |

### Supported Opcodes (30 of 37)

| Category | Opcodes |
|----------|---------|
| Stack/Variables | PUSH, LOAD, STORE, DUP, POP, INC, DEC |
| Arithmetic | ADD, SUB, MUL, DIV, MOD |
| Comparison | EQ, LT, GT |
| Logic | AND, OR, NOT |
| Stack shuffling | SWAP, ROT |
| Control flow | JMP, JZ, JNZ, CALL, RET, HALT, LABEL |
| I/O | PRINT, PRINT\_STR, READ\_INT, EMIT\_CHAR, NEWLINE |

Not yet implemented: PUSH\_STR, READ\_STR, CONCAT, LEN, TO\_INT, TO\_STR (string manipulation operations that have no natural equivalent in ArnoldC's integer-only type system).

### How to Use

```bash
# Generate an ArnoldC interpreter for a MnM program:
python3 generate_mnm_interpreter.py mnm_examples/factorial.mnm mnm_examples/factorial.mnm.json mnm_factorial.arnoldc

# Compile and run:
java -jar ArnoldC.jar mnm_factorial.arnoldc
java mnm_factorial
# Output: 120

# Or from Python:
python3 -c "
from generate_mnm_interpreter import generate
import json
with open('mnm_examples/fizzbuzz.mnm') as f: src = f.read()
with open('mnm_examples/fizzbuzz.mnm.json') as f: sc = json.load(f)
generate(src, sc, output_path='mnm_fizzbuzz.arnoldc')
"
java -jar ArnoldC.jar mnm_fizzbuzz.arnoldc && java mnm_fizzbuzz
# Output: 1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz
```

### MnM Opcode Dispatch (How It Works)

Each iteration of the main loop:
1. Fetches the opcode and operand at the current instruction pointer
2. Checks each opcode via sequential equality tests (`YOU ARE NOT YOU YOU ARE ME`)
3. The matching handler manipulates the stack, variables, and/or control flow
4. If no jump was taken, advances the instruction pointer by 1

For example, MnM's `ADD` (pop two values, push their sum) compiles to ArnoldC that:
- Decrements `sp`, calls `stackRead` to get the top value
- Decrements `sp` again, calls `stackRead` to get the second value
- Computes the sum with `GET UP`
- Calls `condWrite` for each stack cell to write the result at `stack[sp]`
- Increments `sp`

### Known Limitations

- **No same-line output:** `TALK TO THE HAND` always appends a newline. MnM's PRINT and PRINT\_STR each produce a line. NEWLINE is a no-op (since the preceding print already added one).
- **EMIT\_CHAR prints integers:** ArnoldC cannot print characters, so EMIT\_CHAR outputs the numeric value.
- **Generated code size:** ~1400–2100 lines of ArnoldC depending on program complexity.

### Test Results: 35/35 PASS

```bash
python3 test_mnm.py
```

```
  PASS  hello_world          PASS  jz_taken
  PASS  factorial_5          PASS  jz_not_taken
  PASS  fizzbuzz             PASS  jnz_taken
  PASS  halt_only            PASS  jnz_not_taken
  PASS  push_print           PASS  and_true
  PASS  add                  PASS  and_false
  PASS  sub                  PASS  or_true
  PASS  mul                  PASS  countdown
  PASS  div                  PASS  factorial_6
  PASS  mod                  PASS  pop
  PASS  eq_true              PASS  multi_print_str
  PASS  eq_false             PASS  rot
  PASS  gt_true              PASS  swap
  PASS  gt_false             PASS  var_load_store
  PASS  lt_true              PASS  inc_dec
  PASS  lt_false             PASS  jmp
  PASS  not_zero             PASS  dup
  PASS  not_nonzero

35/35 passed
```

### Two approaches: Compiler vs Interpreter

This project implements MnM execution in ArnoldC **two different ways**:

**Approach 1: Compiler** (`generate_mnm_interpreter.py`)

The Python generator produces *different ArnoldC code* per input: different stack sizes, different variable counts, different method signatures, different string tables. The generated ArnoldC doesn't interpret MnM — it *is* the MnM program translated into ArnoldC. This approach supports more MnM features (strings, multiple input queues) and produces faster code, but requires Python at build time.

**Approach 2: True Interpreter** ([`mnm_vm.arnoldc`](mnm_vm.arnoldc))

A single, fixed 7,319-line ArnoldC program that reads **any** MnM program from stdin and executes it — architecturally identical to `brainfuck.arnoldc`. The same file handles factorial, fizzbuzz, countdown, or any program within its limits. No Python in the loop at runtime.

| | `brainfuck.arnoldc` | `mnm_vm.arnoldc` | `generate_mnm_interpreter.py` |
|---|---|---|---|
| **Type** | Interpreter | Interpreter | Compiler |
| **Fixed code?** | Yes (data embedded) | Yes (data from stdin) | No (output varies per input) |
| **Array simulation** | Params to methods | Static fields + GETSTATIC | Params (condWrite pattern) |
| **Limits** | Tape/program pre-sized | 100 instr, 30 stack, 50 vars | Scales to input |
| **String support** | N/A | No | Yes (PRINT\_STR) |
| **Tests** | 38 pass | 16 pass | 35 pass |

### How `mnm_vm.arnoldc` works

The true interpreter required solving every constraint that previously forced the compiler approach:

1. **No arrays → static fields**: all 320+ pre-allocated slots (100 program opcodes, 100 operands, 30 stack cells, 50 variables, 10 call stack, 10 input queue) are stored as JVM static fields. Read/write methods access them via `GETSTATIC`/`PUTSTATIC` through if/else chains — no parameters needed, no 254-param limit.

2. **Program from stdin**: on startup, the interpreter reads integers via `I WANT TO ASK YOU A BUNCH OF QUESTIONS AND I WANT TO HAVE THEM ANSWERED IMMEDIATELY` — first the instruction count, then opcode/operand pairs, then variable initial values, then input queue values. Each value is stored into the corresponding static field via a write method.

3. **Void write methods**: `stackW`, `varW`, `csW` are void methods (no `GIVE THESE PEOPLE AIR`) called with just `DO IT NOW stackW sp val`. No dummy return variables needed.

4. **Fixed opcode dispatch**: the 25 opcode handlers are identical regardless of the input program. Each handler is ~10–15 lines of ArnoldC (just method calls to stackR/stackW/varR/varW), compared to hundreds of lines in the compiler approach.

### Using `mnm_vm.arnoldc`

```bash
# Compile once (requires patched compiler):
java -jar ArnoldC-patched.jar mnm_vm.arnoldc

# Convert any MnM program to stdin format:
python3 mnm_to_stdin.py mnm_examples/factorial.mnm mnm_examples/factorial.mnm.json > /tmp/input.txt

# Run (staggered delivery for ArnoldC's Scanner-per-read quirk):
(while IFS= read -r line; do echo "$line"; sleep 0.1; done < /tmp/input.txt) | java mnm_vm
# Output: 120
```

### Limitations

- **Fixed sizes**: 100 instructions, 30 stack, 50 variables, 10 call stack, 10 input queue. Programs exceeding these limits fail silently. Use the compiler approach for larger programs.
- **No string support**: PRINT\_STR, PUSH\_STR, CONCAT etc. require compile-time string literals. The true interpreter can only handle numeric operations.
- **Stdin delivery**: the patched compiler reuses a shared `Scanner` — piped input works instantly. The original compiler creates a new Scanner per read, requiring staggered delivery.

## Triple Interpreter: ArnoldC → MnM → Brainfuck

The ultimate test: **three esoteric languages interpreting each other**. A Brainfuck program runs inside a MnM interpreter, which runs inside an ArnoldC interpreter, which compiles to JVM bytecode.

There are two approaches to the triple chain — a **compiler** approach (Path 2, fast, Python at build time) and a **true interpreter** approach (Path 4, pure ArnoldC at runtime):

### Path 2: Compiler triple chain

The MnM BF interpreter is compiled into a tailored ArnoldC program by `generate_mnm_interpreter.py`. The ArnoldC varies per input. Python is needed at build time.

```bash
cd demos/triplechain
java -jar ../../ArnoldC-patched.jar mnm_bf_helloworld.arnoldc
java mnm_bf_helloworld
# Output: 72 101 108 108 111 32 87 111 114 108 100 = "Hello World" (6.8s)
```

### Path 4: True interpreter triple chain

A single fixed ArnoldC program (`mnm_vm`) reads the MnM BF interpreter from stdin and executes it. **No Python at runtime** — the same ArnoldC file runs any MnM program, including one that interprets Brainfuck.

```bash
# Build the VM once (sized for the target MnM program):
python3 build_mnm_vm.py mnm_vm_hw.arnoldc --prog 3100 --vars 140 --stack 30
java -jar ArnoldC-patched.jar mnm_vm_hw.arnoldc

# At runtime — pure ArnoldC, no Python:
python3 mnm_to_stdin.py mnm_examples/hw_bf.mnm mnm_examples/hw_bf.mnm.json > input.txt
cat input.txt | java mnm_vm_hw
# Output: 72 101 108 108 111 32 87 111 114 108 100 = "Hello World" (7.2s)
```

### Results

| BF program | BF instr | MnM instr | MnM vars | Path 2 (compiler) | Path 4 (true interp.) |
|-----------|------:|------:|-----:|------:|------:|
| `+++[>++<-]>.` | 12 | 594 | 22 | 0.1s, 12,593 lines | 0.1s, 26,757 lines |
| Hello World | 114 | 3,030 | 130 | 6.8s, 55,747 lines | **7.2s**, 130,055 lines |
| Sierpinski (2 rows) | 124 | 9,610 | 270 | — | **~10 min**, 410,319 lines |
| Sierpinski (32 rows) | 124 | 9,610 | 270 | — | ~2.5 hours (estimated) |

Each level of interpretation adds roughly an order of magnitude in code size, driven by if/else chains simulating array access — because none of the three languages have arrays. See [`demos/triplechain/`](demos/triplechain/) for a detailed walkthrough.

## Coming Full Circle: Direct BF Interpreter (`bf_vm.arnoldc`)

After building the MnM interpreter, the MnM→ArnoldC compiler, the triple chain, patching the ArnoldC compiler three times, and running Sierpinski through 410,000 lines of triple interpretation — we realized we could just build a **direct** BF interpreter in ArnoldC. No MnM in the middle.

[`bf_vm.arnoldc`](bf_vm.arnoldc) (7,281 lines) reads any Brainfuck program from stdin and executes it. No Python at runtime, no intermediate languages:

```bash
java -jar ArnoldC-patched.jar bf_vm.arnoldc    # compile once
echo "12 3 3 3 7 1 3 3 2 4 8 1 5" | java bf_vm  # +++[>++<-]>. → 6
```

This is the **third path** to "ArnoldC runs Brainfuck," and honestly the least interesting:

| Path | Architecture | ArnoldC | What makes it interesting |
|------|-------------|------:|--------------------------|
| **1. `brainfuck.arnoldc`** | Hardcoded BF program | 488 | First interpreter, discovered the 100-var limit |
| **2. Compiler triple chain** | ArnoldC → MnM → BF (Python-compiled) | 55,747 | Tailored per input, supports strings |
| **3. `bf_vm.arnoldc`** | Direct stdin BF interpreter | 7,316 | Any BF from stdin, Sierpinski in 0.2s, chessboard in 4s |
| **4. True triple chain** | ArnoldC → MnM → BF (stdin, no `,`) | 410,319 | Pure ArnoldC, any MnM, any BF — three generic interpreters |
| **5. Triple chain + BF input** | ArnoldC → MnM → BF (`,` compiled per BF) | 51,337 | BF input works, but BF program baked at build time |
| **6. Pure triple chain** | ArnoldC → MnM → BF (all generic, all from stdin) | 290,571 | **The holy grail**: any BF + any input, three fixed interpreters |

**Path 6** is the purest form: one fixed ArnoldC program (290,571 lines) interprets one fixed MnM BF interpreter (4,654 instructions) which reads **any** Brainfuck program **and** its input from stdin at runtime. Three generic interpreters, no Python, all 8 BF instructions including `,`.

```bash
# Hello World through three generic interpreters, no Python:
cat path6_base.txt bf_opcodes.txt | java mnm_vm_path6
# Output: 72 101 108 108 111 32 87 111 114 108 100 = "Hello World"
```

**38/38 test programs pass** through Path 6, including Hello World (111 BF instructions, 5 tape cells — just under the 120/20 limits).

### Path 4 vs Path 6: the purity tradeoff

Path 4 ran Sierpinski because the MnM BF interpreter was **tailored per BF program** — sized with exactly 124 program slots and 140 tape cells. Path 6's MnM interpreter is **fixed** (120 program slots, 20 tape cells) — the same file for every BF program. That's stricter purity but smaller limits.

| | Path 4 (MnM sized per BF) | Path 6 (fixed MnM) |
|---|---|---|
| **MnM interpreter** | Different per BF program | Same for all BF programs |
| **Sierpinski** | Works (140 tape slots) | Doesn't fit (needs 132 tape, limit 20) |
| **Hello World** | Works | Works (111 < 120 prog, 5 < 20 tape) |
| **BF `,` input** | No | Yes |
| **Truly generic?** | MnM varies per BF | Everything fixed |

Could we increase Path 6's limits to fit Sierpinski? We tried. The actual wall is **not** the JVM constant pool (only 3,415 entries used — the ~90K estimate was wrong). It's an **ASM 3.3.1 bytecode generation bug**: `Invalid this class index` when the class file has too many fields/methods. Binary search found the exact boundary:

| Path 6 sizing | PROG | TAPE | MnM vars | ArnoldC lines | Works? | Sierpinski? |
|------|---:|---:|---:|------:|:---:|:---:|
| Default | 120 | 20 | 146 | 290K | Yes | No |
| Max working | 125 | 122 | 263 | 438K | Yes | No (needs 132 tape) |
| Sierpinski-min | 125 | 133 | 264 | 462K | **ASM bug** | Would fit, but crash |

**10 tape cells short.** Fixing this would require upgrading ASM from 3.3.1 (2007) to a modern version — a deeper change to the ArnoldC compiler's bytecode library.

### What the MnM detour actually contributed

An honest assessment: `bf_vm.arnoldc` (Path 3) is **slower** than the original `brainfuck.arnoldc` (Path 1) for the same BF program — 0.068s vs 0.051s. The static fields approach, larger dispatch tables, and stdin parsing all add overhead. The MnM journey didn't improve *performance*. It expanded *capability*:

| | Original `brainfuck.arnoldc` (Path 1) | `bf_vm.arnoldc` (Path 3) |
|---|---|---|
| **Programs** | One, hardcoded at build time | Any, read from stdin at runtime |
| **Max tape cells** | ~50 (100-variable limit) | 150 (configurable, no hard limit) |
| **Max BF instructions** | ~50 (100-variable limit) | 200 (configurable) |
| **Sierpinski triangle** | Impossible (needs 131 tape cells) | 0.2 seconds, complete 32 rows |
| **Compiler required** | Original (unpatched) | Patched (5 fixes from the MnM journey) |
| **Performance** | **Faster** (0.051s for `+++[>++<-]>.`) | Slower (0.068s) |

The original is the faster interpreter for programs that fit within its limits. It just can't run Sierpinski, can't read from stdin, and can't handle programs beyond ~50 instructions+cells.

`bf_vm.arnoldc` **could not have existed** without the MnM journey. MnM's 37-opcode stack machine was harder than BF in every dimension (stack, variables, call stack, strings, input queues), forcing discoveries that BF alone never triggered:

| Capability unlocked | Compiler fix required | Discovered while... |
|--------------------|----------------------|-------------------|
| >100 variables | `COMPUTE_FRAMES` (one-line fix) | MnM BF interpreter needed 150 vars |
| Methods access main-scope state | Static fields (`PUTSTATIC`/`GETSTATIC`) | MnM handler splitting |
| Methods >64KB split automatically | Chunked fetch with nested if/else dispatch | Triple chain with 9,610 MnM instructions |
| Read any program from stdin | Shared Scanner (reuse instead of `new` per read) | Sierpinski stdin delivery was 26 minutes |
| Large programs don't bloat main | Zero-init skip for static fields | 10,000 field declarations exceeded 64KB |
| Correct tape sizing | Simulate BF execution, not static `>` `<` counting | Sierpinski rendered empty (tape too small) |

Without the MnM work: no stdin input, no Sierpinski, no scaling, no programs beyond ~50 vars. Each fix made the BF interpreter more *capable*, not more *fast*.

### Benchmark: `bf_vm` vs Native C Interpreter

We benchmarked `bf_vm.arnoldc` against the reference [`brainfuck`](https://github.com/fabianishere/brainfuck) interpreter (compiled C) across 10 BF programs of varying complexity. All outputs were verified identical.

| Program | Ops | Native C | Cold JVM | Warm JIT | Cold/Ref | Ref/Warm |
|---|---:|---:|---:|---:|---:|---:|
| trivial_print (no loops) | 102 | 2.3 ms | 74 ms | 0.23 ms | 32× | **10×** |
| multiply 3×2 | 12 | 2.3 ms | 70 ms | 0.18 ms | 31× | **13×** |
| countdown 5→1 | 9 | 2.5 ms | 74 ms | 0.16 ms | 29× | **16×** |
| nested multiply 2×3×4 | 22 | 2.8 ms | 79 ms | 0.17 ms | 28× | **16×** |
| Hello World | 106 | 2.5 ms | 90 ms | 0.19 ms | 36× | **13×** |
| alphabet A–Z | 116 | 2.6 ms | 76 ms | 0.20 ms | 29× | **13×** |
| copy cell | 37 | 2.6 ms | 79 ms | 0.22 ms | 30× | **12×** |
| **Sierpinski triangle** | 114 | 2.9 ms | 206 ms | 0.22 ms | 71× | **13×** |
| squares 0,1,4,9,… | 165 | 2.7 ms | 95 ms | 0.23 ms | 35× | **12×** |
| bubble sort cells | 165 | 2.3 ms | 99 ms | 0.24 ms | 43× | **10×** |

**Cold JVM** = separate `java bf_vm` process each time (~70–200 ms, dominated by JVM startup). **Warm JIT** = single JVM, 10 warmup iterations, 30 measured runs via [`BenchBfVm.java`](BenchBfVm.java).

Once HotSpot's JIT compiler warms up, `bf_vm` consistently runs **10–16× faster than the native C interpreter** across all programs. The JIT inlines the dispatch loop, eliminates dead branches in the 7,281-line if/else chain, and compiles the whole thing into tight native code.

A joke language beating a C interpreter is a pretty good punchline.

Reproducible via [`bench_diverse.py`](bench_diverse.py) (end-to-end) or [`BenchBfVm.java`](BenchBfVm.java) (JIT harness only).

## BF Test Suite

The BF interpreter is verified against the reference [`brainfuck`](https://github.com/fabianishere/brainfuck) interpreter (v2.7.3) using [`test_bf.py`](test_bf.py), an automated test harness.

### How It Works

For each test case, the harness:

1. Runs the BF program through the **reference** `brainfuck` interpreter (outputs raw bytes)
2. **Generates** an ArnoldC interpreter with the BF program embedded (`generate_bf_interpreter.py`)
3. **Compiles** the generated `.arnoldc` file to JVM bytecode
4. **Runs** the ArnoldC interpreter (outputs one integer per line)
5. **Compares** outputs: reference bytes are converted to int lists, ArnoldC output lines are parsed as ints, and values are compared with `% 256` normalization

### Running the Tests

```bash
python3 test_bf.py           # run all 38 tests
python3 test_bf.py -v        # verbose output (shows decoded ASCII)
python3 test_bf.py -k hello  # filter tests by name
```

### Test Results: 38/38 PASS

```
============================================================
BF Interpreter Test Suite (38 tests)
============================================================

  [PASS] empty_program
  [PASS] print_zero
  [PASS] single_inc_print
  [PASS] five_incs
  [PASS] inc_dec
  [PASS] move_right_print
  [PASS] move_left_print
  [PASS] multi_cell_print
  [PASS] zigzag_print
  [PASS] multiply_3x2
  [PASS] add_3_5
  [PASS] clear_cell
  [PASS] skip_loop_zero
  [PASS] countdown_print
  [PASS] double_loop
  [PASS] nested_2x2x2
  [PASS] nested_3x3x3
  [PASS] multiply_4x7
  [PASS] multiply_5x2
  [PASS] print_A
  [PASS] print_zero_char
  [PASS] print_newline
  [PASS] only_moves
  [PASS] loop_at_start_skip
  [PASS] nested_skip
  [PASS] back_to_back_loops
  [PASS] hello_world                   <-- 111 BF instructions
  [PASS] add_digits
  [PASS] alphabet_ABC
  [PASS] multiply_6x7_print
  [PASS] squares_1_to_5
  [PASS] cell_copy
  [PASS] print_ABCDEFG
  [PASS] powers_of_2
  [PASS] double_value
  [PASS] tape_setup_4_cells
  [PASS] tape_after_loop
  [PASS] tape_swap

Results: 38 passed, 0 failed, 0 errors, 0 skipped
```

### Test Categories

| Category | # | What is tested |
|----------|---|---------------|
| Trivial | 5 | empty program, print zero, increment, decrement |
| Pointer movement | 4 | `>`, `<`, zigzag, multi-cell prints |
| Simple loops | 6 | multiply, add, clear `[-]`, skip `[` on zero, countdown |
| Nested loops | 4 | 2\*2\*2=8, 3\*3\*3=27, 4\*7=28, 5\*2=10 |
| ASCII output | 3 | print `A` (65), `0` (48), newline (10) |
| Edge cases | 4 | only moves, loop-at-start skip, nested bracket skip, back-to-back loops |
| Real-world | 7 | **Hello World** (111 instr), ABCDEFG, ASCII digits, powers of 2, squares, cell copy |
| Tape verification | 4 | cell setup, post-loop state, swap, double |

## Running the 25 Challenges

### Prerequisites

- Java 8+
- The ArnoldC compiler JAR:

```bash
wget http://lhartikk.github.io/ArnoldC.jar
```

### Compile and Run

```bash
# Compile
java -jar ArnoldC.jar challenges/challenge01.arnoldc

# Run (single input)
echo "5" | java challenge01

# Run (multiple inputs -- needs staggered delivery)
(echo 12; sleep 0.1; echo 9) | java challenge04
```

> **Why `sleep 0.1`?** Each `READ` in ArnoldC creates a new `java.util.Scanner(System.in)`. If all input arrives at once, the first Scanner may consume everything. Staggering with short sleeps ensures each Scanner gets its value.

### Quick Test All

```bash
# Compile everything
for f in challenges/challenge*.arnoldc; do java -jar ArnoldC.jar "$f"; done

# Run selected tests
echo "5"    | java challenge01   # expect: 15
echo "4"    | java challenge02   # expect: 4 3 2 1 0
echo "7"    | java challenge03   # expect: ODD
echo "527"  | java challenge10   # expect: 14
echo "1221" | java challenge17   # expect: YES
echo "6"    | java challenge18   # expect: 8
echo "7"    | java challenge21   # expect: 13
```

## Lessons Learned About ArnoldC

### 1. The Read Statement is a 3-Line Incantation
The documented single-line `I WANT TO ASK YOU A BUNCH OF QUESTIONS AND I WANT TO HAVE THEM ANSWERED IMMEDIATELY var` doesn't work in the actual compiler. Reading from stdin requires:
```
GET YOUR ASS TO MARS variable
DO IT NOW
I WANT TO ASK YOU A BUNCH OF QUESTIONS AND I WANT TO HAVE THEM ANSWERED IMMEDIATELY
```

### 2. No Boolean Literals in Declarations
`YOU SET US UP NO PROBLEMO` fails to parse. Use `YOU SET US UP 0` or `YOU SET US UP 1` instead.

### 3. Variables Inside Branches Cause JVM VerifyError
Declaring variables (`HEY CHRISTMAS TREE`) inside `BECAUSE I'M GOING TO SAY PLEASE` blocks or nested `STICK AROUND` loops can produce JVM bytecode with inconsistent stackmap frames. **Solution:** declare all variables at the top of the scope.

### 4. No Same-Line Printing
`TALK TO THE HAND` maps to Java's `System.out.println()` -- there is no `print()` equivalent. You cannot print two values on the same line. Workarounds used:
- **Staircase (14):** Print numbers made of 1s (1, 11, 111, 1111)
- **Histogram (23):** Print label then count of 1s on separate lines
- **Caesar cipher (25):** Output shifted ASCII codes as integers
- **BF interpreter:** Output cell values as integers instead of characters

### 5. No `<=` Operator
ArnoldC only has `>` (`LET OFF SOME STEAM BENNET`) and `==` (`YOU ARE NOT YOU YOU ARE ME`). To check `i <= n`, compute `(n + 1) > i`. To negate a boolean, compute `1 - value`.

### 6. Recursion Works
Methods compile to JVM methods, so recursive calls (challenge 21 -- Fibonacci) work naturally via the JVM call stack.

### 7. Hard Limit: 100 Local Variables Per Method (Fixable!)
ArnoldC's bytecode generator breaks when a method has more than **100 local variables** (parameters + declared variables). At exactly 101 locals, compilation succeeds but the JVM rejects the class with `StackMapTable format error` or `Arguments can't fit into locals`. This was discovered while building the BF interpreter: storing 111 program slots as main-method variables failed. **Workaround:** hardcode program data as constants inside a method's if/else chain, removing the variables entirely.

**Root cause:** The limit comes from a hardcoded `visitMaxs(100, 100)` in three places in the ArnoldC source (`MainMethodNode.scala`, `MethodNode.scala`, `RootNode.scala`), combined with `ClassWriter(0)` which tells ASM to trust these values instead of computing them. The JVM itself supports up to 65,535 local variables. This bug was never reported in ArnoldC's issue tracker — nobody had pushed the language this far before.

**Fixes:** (1) Changing `ClassWriter(0)` to `ClassWriter(ClassWriter.COMPUTE_FRAMES)` removes the 100-variable limit. (2) Storing main-scope variables as static fields (`PUTSTATIC`/`GETSTATIC` instead of `ISTORE`/`ILOAD`) lets methods access them directly, enabling handler splitting that defeats the JVM's 64KB method body limit. Both fixes are included in `ArnoldC-patched.jar`. Programs with 150+ variables now compile and run correctly. See [Patching the ArnoldC Compiler](#patching-the-arnoldc-compiler) for the full story.

### 8. The Tiny VM is Peak ArnoldC
Challenge 22 implements a virtual machine *inside* an esoteric language. The VM supports 6 opcodes (PUSH, ADD, SUB, MUL, PRINT, HALT) using a chain of equality checks -- essentially a switch-case built from `YOU ARE NOT YOU YOU ARE ME`.

## Patching the ArnoldC Compiler

While building interpreters for MnM and Brainfuck, we hit ArnoldC's 100-local-variable limit repeatedly — it shaped the entire architecture of the generators and forced careful variable budgeting. Eventually we dug into the compiler source to find out why.

### The discovery

The MnM BF interpreter from [acherm/mnmlang](https://github.com/acherm/mnmlang) uses 150 variables (10 control + 20 program slots + 120 tape cells). Feeding it through `generate_mnm_interpreter.py` produces 33,099 lines of ArnoldC — which crashes the compiler:

```
Exception in thread "main" java.lang.NullPointerException
    at org.objectweb.asm.Frame.a(Unknown Source)
```

A simpler test — 120 variables, no control flow — compiles but fails at runtime:

```
java.lang.VerifyError: Local variable table overflow
    Local index 100 is invalid
```

The JVM itself supports 65,535 local variables. The limit is purely in ArnoldC's bytecode generator.

### Root cause: hardcoded `visitMaxs(100, 100)`

The ArnoldC compiler (written in Scala, using ASM 3.3.1 for bytecode generation) has the value 100 hardcoded in three places:

```scala
// MainMethodNode.scala:17
mv.visitMaxs(100, 100)

// MethodNode.scala:24
mv.visitMaxs(100, 100)

// RootNode.scala:40
mv.visitMaxs(100, 100)
```

And the `ClassWriter` is created with flag `0` — meaning ASM trusts these values instead of computing them:

```scala
// RootNode.scala:29
val cw = new ClassWriter(0)   // no COMPUTE_MAXS, no COMPUTE_FRAMES
```

When a method uses local slot 100+, the JVM sees `max_locals=100` in the Code attribute but the bytecode references higher slots, which is invalid. With control flow (while/if-else), the failure mode is worse: manually emitted StackMapTable entries declare the actual variable count, conflicting with the declared `max_locals=100`.

### Is this a known issue?

**No.** We searched all ~70 open/closed issues on [github.com/lhartikk/ArnoldC](https://github.com/lhartikk/ArnoldC/issues) — none mention variable limits, `visitMaxs`, StackMapTable, or anything related. The project has been dormant since ~2015. Web searches also returned nothing. Nobody had pushed an esoteric joke language to 100+ variables before.

### The fix: one line

```diff
- val cw = new ClassWriter(0)
+ val cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES)
```

With `COMPUTE_FRAMES`, ASM automatically computes correct `max_locals`, `max_stack`, and StackMapTable entries from the actual bytecode. The hardcoded `visitMaxs(100, 100)` and all 14 manual `visitFrame()` calls across 8 source files become effectively no-ops.

### Results (COMPUTE_FRAMES only)

| Variables | Original compiler | COMPUTE_FRAMES patch |
|-----------|-------------------|----------------------|
| ≤ 100 | Works | Works |
| 120 | `VerifyError: Local index 100 is invalid` | Works correctly |
| 150 | `NullPointerException` in ASM | Compiles, but hits JVM's 64KB method body limit |
| All 73 tests | 73/73 pass | 73/73 pass |

This fixes the 100-variable limit but reveals a second wall: the JVM specification requires method bodies to be under 65,535 bytes (§4.7.3). With 150 variables and 30 opcode handlers each containing N `condWrite` calls, the main method generates 70,016 bytes — just over the limit.

### Defeating the 64KB method limit: static fields + handler splitting

The 64KB limit is a hard JVM spec constraint, but it's per-method. The fix is to **split the main method** by moving opcode handlers into separate methods. This requires a second compiler change: storing main-scope variables as **static fields** instead of local variables.

With local variables (`ISTORE`/`ILOAD`), called methods cannot access the caller's state — every value must be passed as a parameter and returned. With static fields (`PUTSTATIC`/`GETSTATIC`), any method can read and write main-scope variables directly, making handler splitting trivial.

**Compiler changes** (7 files modified in the ArnoldC Scala source):
- `SymbolTable.scala`: tracks which variables are fields, adds `emitVarLoad`/`emitVarStore` helpers that emit `GETSTATIC`/`PUTSTATIC` for main-scope variables and `ILOAD`/`ISTORE` for method-local parameters
- `RootNode.scala`: enables field mode, calls `ClassWriter.visitField` for each main-scope variable
- `DeclareIntNode.scala`, `VariableNode.scala`, `AssignVariableNode.scala`, `CallMethodNode.scala`, `CallReadMethodNode.scala`: use `emitVarLoad`/`emitVarStore` instead of raw `ILOAD`/`ISTORE`

**Generator change** (`generate_mnm_interpreter.py`): new `static_fields=True` mode. Each opcode handler becomes a separate ArnoldC method. The main loop shrinks to: fetch instruction → check opcode → call handler method → advance ip. Each handler method accesses `sp`, `s0`–`sN`, `v0`–`vK`, `jumped`, etc. as static fields.

### Final results

| Variables | Original | COMPUTE_FRAMES | + Static fields |
|-----------|----------|----------------|-----------------|
| ≤ 100 | Works | Works | Works |
| 120 | `VerifyError` | Works | Works |
| 150 | `NullPointerException` | 64KB method limit | **Works** |
| All 73 tests | 73/73 pass | 73/73 pass | 73/73 pass |

The 150-variable MnM BF interpreter (33,281 lines of ArnoldC) now compiles and runs correctly, producing the expected output. The patched compiler (`ArnoldC-patched.jar`) includes both fixes.

### Building the patched compiler

The ArnoldC project dates from ~2014 and its build config needs modernization. Three things must be fixed: the one-line compiler patch, outdated SBT plugin versions, and an unavailable speech synthesis dependency.

**1. Clone and apply the fixes:**

```bash
git clone https://github.com/lhartikk/ArnoldC.git
cd ArnoldC

# Fix 1: COMPUTE_FRAMES (removes 100-variable limit)
sed -i '' 's/new ClassWriter(0)/new ClassWriter(ClassWriter.COMPUTE_FRAMES)/' \
  src/main/scala/org/arnoldc/ast/RootNode.scala
```

For the static fields fix (removes 64KB method limit), the changes to `SymbolTable.scala` and the 5 AST node files are more extensive — see the [patched source files](https://github.com/acherm/agentic-arnoldc) or the commit history for the full diff. The key change is replacing every `mv.visitVarInsn(ISTORE, symbolTable.getVariableAddress(var))` with `symbolTable.emitVarStore(mv, var)` (and likewise for `ILOAD` → `emitVarLoad`), where the new methods choose between field and local access based on scope.

**2. Update SBT plugins** (`project/plugins.sbt`): the original uses `sbt-idea 1.5.1` (defunct IntelliJ plugin) and `sbt-assembly 0.10.1` (incompatible with modern SBT). Replace with:

```sbt
addSbtPlugin("com.eed3si9n" % "sbt-assembly" % "2.1.1")
```

**3. Remove speech synthesis dependency:** ArnoldC includes a `-declaim` feature that uses FreeTTS/JSAPI to speak programs in Arnold's voice. These libraries are no longer available in public Maven repositories. The solution is to remove the FreeTTS dependencies from `build.sbt` and stub out `Declaimer.scala`:

In `build.sbt`, remove the `javax.speech` and `org.mobicents.external.freetts` dependencies and the `"Speech"` resolver. Replace the `assemblySettings` / `AssemblyKeys._` imports (old sbt-assembly API) with:

```sbt
assembly / mainClass := Some("org.arnoldc.ArnoldC")
assembly / assemblyMergeStrategy := {
  case PathList("META-INF", _*) => MergeStrategy.discard
  case _ => MergeStrategy.first
}
```

Replace `src/main/scala/org/arnoldc/Declaimer.scala` with a stub:

```scala
package org.arnoldc
import org.arnoldc.ast._
object Declaimer {
  def declaim(root: RootNode, outputFile: String): Unit =
    throw new UnsupportedOperationException("Speech synthesis not available in patched build")
}
```

**4. Build:**

```bash
sbt assembly
# Output: target/scala-2.11/ArnoldC-assembly-*.jar
```

The resulting JAR is ~6 MB (vs 12 MB original, since FreeTTS is gone). All compiler functionality is preserved — only the `-declaim` speech feature is disabled.

## How This Was Made

All programs were generated by **Claude (Anthropic)**:

1. **25 challenges:** Five parallel AI agents each tackled a batch of 5 challenges, writing `.arnoldc` source, compiling with the real compiler, and verifying outputs
2. **Brainfuck interpreter:** Designed an architecture to simulate arrays via method parameter passing, wrote a Python generator for the repetitive ArnoldC code, and iterated through compilation errors
3. **100-local-variable discovery:** Empirical testing revealed ArnoldC's bytecode generator fails above 100 locals per method. Redesigned the interpreter to hardcode program data as constants rather than variables
4. **BF test suite:** Built an automated harness comparing ArnoldC BF output against the reference `brainfuck` interpreter across 38 test cases covering 8 categories, from trivial programs to Hello World (111 instructions)
5. **MnM Lang interpreter:** Extended the generator architecture to handle MnM Lang's 30-opcode stack machine — stack, variables, call stack, input queues, and string output — all simulated in ArnoldC's integer-only type system. Verified with 35 automated tests
6. **Triple interpreter chain:** Built `generate_mnm_bf.py` to create minimal MnM BF interpreters for specific BF programs, achieving ArnoldC interpreting MnM interpreting Brainfuck. Worked around ArnoldC's 100-local-variable limit by generating tailored, compact programs
7. **Compiler patches:** Traced the 100-variable limit to a hardcoded `visitMaxs(100, 100)` — one-line fix. Then hit the JVM 64KB method body limit at 150 variables. Solved by a deeper compiler change: main-scope variables stored as static fields (`PUTSTATIC`/`GETSTATIC`) so handler methods can access them directly, enabling method splitting. Both bugs were never reported — first known diagnosis and fix
8. **True MnM interpreter:** Recognized that the compiler approach (`generate_mnm_interpreter.py`) was architecturally different from the BF interpreter — it generated different ArnoldC per input, not a fixed program. Built `mnm_vm.arnoldc`: a single 7,319-line ArnoldC program that reads any MnM program from stdin and executes it. Uses static fields for all state (320+ pre-allocated slots), void write methods, and GETSTATIC-based reads — eliminating every limit that previously forced the compiler approach. Verified with 16 automated tests
9. **Sierpinski triangle:** Ran the Sierpinski BF program through the triple chain (ArnoldC→MnM→BF). Required three more compiler fixes: shared Scanner (no staggered stdin delivery), zero-init skip (main method under 64KB), nested if/else dispatch (correct chunk routing). First 6 rows rendered in 30 minutes through 410,319 lines of ArnoldC
10. **True triple chain (Path 4):** Combined `mnm_vm` with a MnM BF interpreter: a single fixed ArnoldC program reads MnM from stdin, which itself interprets Brainfuck. Hello World in 7.2 seconds through 130K lines. Sierpinski renders (slowly — ~10 min for 2 rows) through 410K lines. No Python at runtime — the purest form of three nested interpreters
11. **Coming full circle (Path 3):** Realized the MnM layer was unnecessary for BF interpretation. Built `bf_vm.arnoldc` — a direct ArnoldC→BF interpreter (7,281 lines). Sierpinski in 0.2 seconds. The least interesting path, but it only exists because the MnM detour forced all the compiler patches
12. **Complete BF (all 8 instructions):** Implemented `,` (BF input) in `bf_vm.arnoldc`. The shared Scanner reads program data from stdin first, then runtime input for `,` instructions from the same stream. Verified with echo loops, arithmetic on inputs, rot13.b (840 instructions), and chessboard.b (1,092 instructions rendering a full chess position from FEN input). Added 8-bit cell wrapping (`% 256`) for correct behavior of programs relying on byte overflow
13. **Triple chain with BF input (Path 5):** Added `,` support to the MnM BF interpreter (`generate_mnm_bf.py`): BF `,` emits MnM `READ_INT`, which reads from the MnM input queue, which is pre-loaded from stdin. Runtime input flows through three interpreter levels with no Python. But this broke Path 4's purity: the MnM BF interpreter is now compiled per BF program (comparison chains sized to the specific program), so the BF program is baked at build time. Chessboard attempted but hits the JVM 65K constant pool limit (53K fields needed). Multiply demo works: `./run.sh 6 7 → 42`
14. **Pure triple chain (Path 6):** Built `build_mnm_bf_generic.py` to generate a FIXED MnM BF interpreter (always the same, 4,654 instructions) that reads any BF program + input from the MnM input queue at runtime. Combined with `mnm_vm` (290K lines), this achieves three fixed generic interpreters: ArnoldC interprets MnM interprets BF, any program, any input, no Python. 38/38 test programs pass including Hello World (111 instructions). Sierpinski doesn't fit (needs 132 tape cells, limit 20) — increasing limits hits the JVM 65K constant pool wall

## Where We Are

The project started with 25 ArnoldC programming challenges and evolved into a deep exploration of language interpretation, compiler internals, and the limits of esoteric programming.

### What exists

| Artifact | Lines | What it does | Tests |
|----------|------:|-------------|-------|
| `brainfuck.arnoldc` | 488 | BF interpreter (one hardcoded program) | 38/38 |
| `bf_vm.arnoldc` | 7,316 | BF interpreter (any program from stdin, all 8 instructions) | 38/38 + chessboard + rot13 |
| `mnm_vm.arnoldc` | 7,319 | MnM interpreter (any MnM program from stdin) | 16/16 |
| `generate_mnm_interpreter.py` | — | MnM→ArnoldC compiler | 35/35 |
| `ArnoldC-patched.jar` | — | ArnoldC compiler with 6 fixes | all 127 tests pass |
| `test_triplechain.py` | — | BF via true triple chain (ArnoldC→MnM→BF) | 38/38 |
| `benchmark_bf.py` | — | All 6 execution paths benchmarked | 14 programs |
| 25 challenges | ~1,500 | Programming challenges in ArnoldC | 25/25 |

### What works

- **Sierpinski triangle** in 0.2s (`bf_vm`) or ~10 min per row (Path 4 triple chain)
- **Chess position rendering** from any FEN string in ~4s (`bf_vm` + chessboard.b)
- **rot13** encryption (840 BF instructions, uses `,` for input)
- **Hello World** through 3 fixed generic interpreters (Path 6) — no Python at runtime
- **38/38 BF test programs** identical output across all execution paths
- **38/38 BF test programs** fit in Path 6 (pure triple chain, ≤120 instr, ≤20 tape)

### The six paths to "ArnoldC runs Brainfuck"

| Path | Architecture | Any BF? | BF `,`? | Python? | Generic interpreters? |
|------|-------------|:---:|:---:|:---:|:---:|
| **1** | Hardcoded BF in ArnoldC | No | No | No | N/A |
| **2** | Compiled triple chain | No | No | Build | 1 (ArnoldC; MnM+BF compiled) |
| **3** | Direct BF interpreter (`bf_vm`) | **Yes** | **Yes** | No | 1 (ArnoldC) |
| **4** | True triple chain | **Yes** | No | No | 3 (but MnM sized per BF) |
| **5** | Triple chain + BF input | No | **Yes** | No | 2 (BF compiled into MnM) |
| **6** | **Pure triple chain** | **Yes** | **Yes** | **No** | **3 (all fixed)** |

Path 6 is the purest: three fixed interpreters (ArnoldC + MnM + BF), any BF program, any BF input, no Python at runtime. The cost is smaller limits (120 BF instructions, 20 tape cells) imposed by the JVM constant pool ceiling. Path 3 remains the most capable (Sierpinski, chessboard, rot13) but skips the MnM layer.

### The six compiler patches

| # | Fix | What it solved | Discovered while... |
|---|-----|---------------|-------------------|
| 1 | `ClassWriter(COMPUTE_FRAMES)` | 100-variable limit | MnM needed 150 vars |
| 2 | Static fields (`PUTSTATIC`/`GETSTATIC`) | Methods can't access main state | Splitting MnM handlers |
| 3 | Shared Scanner | 26-minute stdin delivery | Sierpinski through triple chain |
| 4 | Zero-init skip | 10,000 field inits exceed 64KB | Large program slots |
| 5 | Nested if/else dispatch | Chunk boundary overwrites | Programs > 2000 instructions |
| 6 | 8-bit cell wrapping | BF programs relying on byte overflow | Chessboard missing rank |

### Remaining limitations

- **No character output**: `TALK TO THE HAND` prints integers, not characters. Output needs post-processing to decode ASCII.
- **No MnM strings**: the true MnM interpreter (`mnm_vm`) can't do PRINT\_STR, CONCAT, etc. The compiler approach supports them.
- **Fixed sizes**: `bf_vm` defaults to 200 program slots / 150 tape cells (configurable via `build_bf_vm.py`).
- **Performance**: the triple chain is ~2,400× slower than a native C BF interpreter. The direct `bf_vm` is ~29× slower (dominated by JVM startup).
- **Interactive programs**: `,` works for pre-provided input, but true interactive I/O (reading keystrokes mid-execution) isn't practical through piped stdin.

## License

These programs are released into the public domain. Do whatever you want with them. Arnold would approve.

> "I'll be back." -- to write more ArnoldC, probably.
