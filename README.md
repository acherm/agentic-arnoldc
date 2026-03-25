# Agentic ArnoldC

25 programming challenges, a Brainfuck interpreter, and an automated test suite -- all in **[ArnoldC](https://github.com/lhartikk/ArnoldC)**, the esoteric programming language where every keyword is an Arnold Schwarzenegger movie quote.

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
├── challenge01.arnoldc .. challenge25.arnoldc   # 25 programming challenges
├── brainfuck.arnoldc                            # BF interpreter (generated)
├── generate_bf_interpreter.py                   # Python generator for BF interpreter
├── test_bf.py                                   # Automated test suite (38 tests)
└── README.md
```

## The 25 Challenges

### Easy (1-10)

| # | Challenge | File | Description | Example |
|---|-----------|------|-------------|---------|
| 1 | Sum 1 to N | [`challenge01.arnoldc`](challenge01.arnoldc) | Read n, print 1+2+...+n | 5 &rarr; 15 |
| 2 | Countdown | [`challenge02.arnoldc`](challenge02.arnoldc) | Print n down to 0 | 4 &rarr; 4,3,2,1,0 |
| 3 | Even or Odd | [`challenge03.arnoldc`](challenge03.arnoldc) | Print EVEN or ODD | 7 &rarr; ODD |
| 4 | Max of Two | [`challenge04.arnoldc`](challenge04.arnoldc) | Print the larger of two integers | 12,9 &rarr; 12 |
| 5 | Absolute Value | [`challenge05.arnoldc`](challenge05.arnoldc) | Print \|n\| | -8 &rarr; 8 |
| 6 | Multiplication Table | [`challenge06.arnoldc`](challenge06.arnoldc) | Print n*1 through n*10 | 3 &rarr; 3,6,...,30 |
| 7 | Power of Two | [`challenge07.arnoldc`](challenge07.arnoldc) | Print 2^0 through 2^n | 4 &rarr; 1,2,4,8,16 |
| 8 | Multiply w/o `*` | [`challenge08.arnoldc`](challenge08.arnoldc) | Repeated addition only | 4,3 &rarr; 12 |
| 9 | Integer Average | [`challenge09.arnoldc`](challenge09.arnoldc) | Print (a+b)/2 | 7,10 &rarr; 8 |
| 10 | Sum of Digits | [`challenge10.arnoldc`](challenge10.arnoldc) | Sum decimal digits | 527 &rarr; 14 |

### Easy/Medium -- Original (11-20)

| # | Challenge | File | Description | Example |
|---|-----------|------|-------------|---------|
| 11 | Total Counter | [`challenge11.arnoldc`](challenge11.arnoldc) | Sum of 6 integers | 3,4,2,5,1,6 &rarr; 21 |
| 12 | Largest Category | [`challenge12.arnoldc`](challenge12.arnoldc) | Find label (A-F) with highest count | 3,9,2,5,1,6 &rarr; B |
| 13 | Vending Machine | [`challenge13.arnoldc`](challenge13.arnoldc) | Greedy coin change | 68 &rarr; 2Q,1D,1N,3P |
| 14 | Staircase | [`challenge14.arnoldc`](challenge14.arnoldc) | Print staircase pattern | 4 &rarr; 1,11,111,1111 |
| 15 | String Length | [`challenge15.arnoldc`](challenge15.arnoldc) | Count integers until sentinel 0 | 9 codes + 0 &rarr; 9 |
| 16 | Repeat Phrase | [`challenge16.arnoldc`](challenge16.arnoldc) | Print HELLO k times | 3 &rarr; HELLO x3 |
| 17 | Palindrome | [`challenge17.arnoldc`](challenge17.arnoldc) | Check if number is palindrome | 1221 &rarr; YES |
| 18 | Collatz Steps | [`challenge18.arnoldc`](challenge18.arnoldc) | Count Collatz steps to 1 | 6 &rarr; 8 |
| 19 | Run-Length Decode | [`challenge19.arnoldc`](challenge19.arnoldc) | Expand (count,value) pairs | 3,65,2,66 &rarr; 65x3,66x2 |
| 20 | Mini Gradebook | [`challenge20.arnoldc`](challenge20.arnoldc) | Min, max, average of 5 grades | 12,8,15,10,14 &rarr; 8,15,11 |

### Hard + Bonus (21-25)

| # | Challenge | File | Description | Example |
|---|-----------|------|-------------|---------|
| 21 | Recursive Fibonacci | [`challenge21.arnoldc`](challenge21.arnoldc) | fib(n) via recursive method | 7 &rarr; 13 |
| 22 | Tiny Virtual Machine | [`challenge22.arnoldc`](challenge22.arnoldc) | Interpreter for PUSH/ADD/SUB/MUL/PRINT/HALT | PUSH 5, PRINT &rarr; 5 |
| 23 | Text Histogram | [`challenge23.arnoldc`](challenge23.arnoldc) | Bar chart for 6 labeled counts | 2,4,1,... &rarr; A:2, B:4,... |
| 24 | Digital Clock Tick | [`challenge24.arnoldc`](challenge24.arnoldc) | Advance time by one second | 23:59:59 &rarr; 0:0:0 |
| 25 | Caesar Cipher | [`challenge25.arnoldc`](challenge25.arnoldc) | Shift ASCII codes by k | shift 3, CODE &rarr; FRGH |

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

## Test Suite

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
java -jar ArnoldC.jar challenge01.arnoldc

# Run (single input)
echo "5" | java challenge01

# Run (multiple inputs -- needs staggered delivery)
(echo 12; sleep 0.1; echo 9) | java challenge04
```

> **Why `sleep 0.1`?** Each `READ` in ArnoldC creates a new `java.util.Scanner(System.in)`. If all input arrives at once, the first Scanner may consume everything. Staggering with short sleeps ensures each Scanner gets its value.

### Quick Test All

```bash
# Compile everything
for f in challenge*.arnoldc; do java -jar ArnoldC.jar "$f"; done

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

### 7. Hard Limit: 100 Local Variables Per Method
ArnoldC's bytecode generator breaks when a method has more than **100 local variables** (parameters + declared variables). At exactly 101 locals, compilation succeeds but the JVM rejects the class with `StackMapTable format error` or `Arguments can't fit into locals`. This was discovered while building the BF interpreter: storing 111 program slots as main-method variables failed. **Solution:** hardcode program data as constants inside a method's if/else chain, removing the variables entirely.

### 8. The Tiny VM is Peak ArnoldC
Challenge 22 implements a virtual machine *inside* an esoteric language. The VM supports 6 opcodes (PUSH, ADD, SUB, MUL, PRINT, HALT) using a chain of equality checks -- essentially a switch-case built from `YOU ARE NOT YOU YOU ARE ME`.

## How This Was Made

All programs were generated by **Claude (Anthropic)** in a single conversation:

1. **25 challenges:** Five parallel AI agents each tackled a batch of 5 challenges, writing `.arnoldc` source, compiling with the real compiler, and verifying outputs
2. **Brainfuck interpreter:** Designed an architecture to simulate arrays via method parameter passing, wrote a Python generator for the repetitive ArnoldC code, and iterated through compilation errors
3. **100-local-variable discovery:** Empirical testing revealed ArnoldC's bytecode generator fails above 100 locals per method. Redesigned the interpreter to hardcode program data as constants rather than variables.
4. **Test suite:** Built an automated harness comparing ArnoldC BF output against the reference `brainfuck` interpreter across 38 test cases covering 8 categories, from trivial programs to Hello World (111 instructions)

## License

These programs are released into the public domain. Do whatever you want with them. Arnold would approve.

> "I'll be back." -- to write more ArnoldC, probably.
