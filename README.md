# Agentic ArnoldC

25 programming challenges, a Brainfuck interpreter, an MnM Lang interpreter, and automated test suites -- all in **[ArnoldC](https://github.com/lhartikk/ArnoldC)**, the esoteric programming language where every keyword is an Arnold Schwarzenegger movie quote.

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
├── brainfuck.arnoldc                                # BF interpreter (generated)
├── generate_bf_interpreter.py                       # Python generator for BF interpreter
├── test_bf.py                                       # Automated test suite (38 BF tests)
├── generate_mnm_interpreter.py                      # Python generator for MnM Lang interpreter
├── generate_mnm_bf.py                               # BF→MnM→ArnoldC triple-chain generator
├── test_mnm.py                                      # Automated test suite (35 MnM tests)
├── mnm_examples/                                    # MnM Lang example programs
│   ├── hello_world.mnm / .mnm.json
│   ├── factorial.mnm / .mnm.json
│   └── fizzbuzz.mnm / .mnm.json
├── ArnoldC-patched.jar                              # Patched compiler (100-var limit removed)
├── demo/                                            # Pre-built artifacts for all interpreter chains
│   ├── README.md                                    # Detailed walkthrough
│   ├── bf_program.txt                               # Input BF program: +++[>++<-]>.
│   ├── bf_interpreter.mnm / .mnm.json               # MnM BF interpreter (594 lines)
│   ├── mnm_bf_interpreter.arnoldc                   # ArnoldC interpreting MnM interpreting BF (12,411 lines)
│   ├── mnm_hello_world.arnoldc                      # ArnoldC interpreting MnM hello world
│   ├── mnm_factorial.arnoldc                        # ArnoldC interpreting MnM factorial
│   └── mnm_fizzbuzz.arnoldc                         # ArnoldC interpreting MnM fizzbuzz
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

The MnM interpreter follows the same architecture as the Brainfuck interpreter: a Python generator ([`generate_mnm_interpreter.py`](generate_mnm_interpreter.py)) takes a `.mnm` program + sidecar and produces a tailored ArnoldC file that executes it.

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

## Triple Interpreter: ArnoldC → MnM → Brainfuck

The ultimate test: **three esoteric languages interpreting each other**. A Brainfuck program runs inside a MnM interpreter, which runs inside an ArnoldC interpreter, which compiles to JVM bytecode.

```
Brainfuck          MnM Lang           ArnoldC             JVM
+++[>++<-]>.  ──▶  594 instructions  ──▶  12,411 lines  ──▶  output: 6
 (12 instr)        (22 variables)        (Arnie quotes)
```

```bash
# Try it yourself:
python3 generate_mnm_bf.py '+++[>++<-]>.' --run
# Output: 6  (computes 3×2)

# Or compile and run the pre-built artifact:
cd demo
java -jar ../ArnoldC.jar mnm_bf_interpreter.arnoldc
java mnm_bf_interpreter
# Output: 6
```

Each level of interpretation adds roughly an order of magnitude in code size, driven by if/else chains simulating array access — because none of the three languages have arrays. See [`demo/README.md`](demo/README.md) for a detailed walkthrough of the architecture, size explosion, and design constraints.

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

**One-line fix:** Changing `ClassWriter(0)` to `ClassWriter(ClassWriter.COMPUTE_FRAMES)` in `RootNode.scala` lets ASM automatically compute correct `max_locals`, `max_stack`, and StackMapTable entries. A patched JAR (`ArnoldC-patched.jar`) is included in this repository and passes all 73 tests. Programs with 120+ variables compile and run correctly. The remaining hard limit is the JVM's own 64KB method body size, which kicks in around 150+ variables with complex control flow.

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

### Results

| Variables | Original compiler | Patched compiler |
|-----------|-------------------|------------------|
| ≤ 100 | Works | Works |
| 120 | `VerifyError: Local index 100 is invalid` | Works correctly |
| 150 | `NullPointerException` in ASM | Compiles, but hits JVM's 64KB method body limit |
| All 73 tests | 73/73 pass | 73/73 pass |

The patched compiler (`ArnoldC-patched.jar`) is included in this repository. The remaining hard limit is the JVM's own 64KB method body size — when a main loop with 150+ variable `condWrite` calls generates more than 65,535 bytes of bytecode, the JVM rejects the class. This is not fixable in ArnoldC; it's a JVM specification constraint. It's why the generator approach (producing compact, tailored programs) remains valuable even with the patch.

### Building the patched compiler

The ArnoldC project dates from ~2014 and its build config needs modernization. Three things must be fixed: the one-line compiler patch, outdated SBT plugin versions, and an unavailable speech synthesis dependency.

**1. Clone and apply the bytecode fix:**

```bash
git clone https://github.com/lhartikk/ArnoldC.git
cd ArnoldC

sed -i '' 's/new ClassWriter(0)/new ClassWriter(ClassWriter.COMPUTE_FRAMES)/' \
  src/main/scala/org/arnoldc/ast/RootNode.scala
```

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
7. **Compiler patch:** Traced the 100-variable limit to a hardcoded `visitMaxs(100, 100)` in the ArnoldC Scala source. One-line fix (`ClassWriter(0)` → `ClassWriter(ClassWriter.COMPUTE_FRAMES)`) eliminates the limit entirely. Never reported before — first known diagnosis and fix of this bug

## License

These programs are released into the public domain. Do whatever you want with them. Arnold would approve.

> "I'll be back." -- to write more ArnoldC, probably.
