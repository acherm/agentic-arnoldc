# Agentic ArnoldC: 25 Programming Challenges in an Esoteric Language

**All 25 programs were written, compiled, and verified by AI agents (Claude) using the [ArnoldC](https://github.com/lhartikk/ArnoldC) esoteric programming language** -- a language where every keyword is an Arnold Schwarzenegger movie quote.

> "IT'S SHOWTIME" = begin program. "YOU HAVE BEEN TERMINATED" = end program. "TALK TO THE HAND" = print. You get the idea.

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

## Running the Programs

### Prerequisites

- Java 8+ (the compiler generates JVM bytecode)
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
The documented single-line `I WANT TO ASK YOU A BUNCH OF QUESTIONS AND I WANT TO HAVE THEM ANSWERED IMMEDIATELY var` doesn't work in the actual compiler. Instead, reading from stdin requires:
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
`TALK TO THE HAND` maps to Java's `System.out.println()` -- there is no `print()` equivalent. This means you cannot print two values on the same line. Workarounds used:
- **Staircase (14):** Print numbers made of 1s (1, 11, 111, 1111)
- **Histogram (23):** Print label then count of 1s on separate lines
- **Caesar cipher (25):** Output shifted ASCII codes as integers

### 5. No `<=` Operator
ArnoldC only has `>` (`LET OFF SOME STEAM BENNET`) and `==` (`YOU ARE NOT YOU YOU ARE ME`). To check `i <= n`, compute `(n + 1) > i`. To negate a boolean, compute `1 - value`.

### 6. Recursion Works
Methods compile to JVM methods, so recursive calls (challenge 21 -- Fibonacci) work naturally via the JVM call stack.

### 7. The Tiny VM is Peak ArnoldC
Challenge 22 implements an interpreter *inside* an esoteric language. The VM supports 6 opcodes (PUSH, ADD, SUB, MUL, PRINT, HALT) using a chain of equality checks -- essentially a switch-case built from `YOU ARE NOT YOU YOU ARE ME`.

## How This Was Made

All 25 programs were generated by **Claude (Anthropic)** in a single conversation:
1. Five parallel AI agents each tackled a batch of 5 challenges
2. Each agent wrote the `.arnoldc` source, compiled it with the real compiler, and verified outputs
3. Compilation errors were debugged iteratively (notably: the read syntax, variable scoping, and boolean literal issues)

The entire process -- from challenge specification to 25 working, tested programs -- was completed in one shot.

## Test Results

```
Challenge 01 (Sum 1 to N)           PASS    echo "5"    -> 15
Challenge 02 (Countdown)            PASS    echo "4"    -> 4,3,2,1,0
Challenge 03 (Even or Odd)          PASS    echo "7"    -> ODD
Challenge 04 (Max of Two)           PASS    12,9        -> 12
Challenge 05 (Absolute Value)       PASS    echo "-8"   -> 8
Challenge 06 (Multiplication Table) PASS    echo "3"    -> 3,6,...,30
Challenge 07 (Power of Two)         PASS    echo "4"    -> 1,2,4,8,16
Challenge 08 (Multiply w/o *)       PASS    4,3         -> 12
Challenge 09 (Integer Average)      PASS    7,10        -> 8
Challenge 10 (Sum of Digits)        PASS    echo "527"  -> 14
Challenge 11 (Total Counter)        PASS    3,4,2,5,1,6 -> 21
Challenge 12 (Largest Category)     PASS    3,9,2,5,1,6 -> B
Challenge 13 (Vending Machine)      PASS    echo "68"   -> 2Q,1D,1N,3P
Challenge 14 (Staircase)            PASS    echo "4"    -> 1,11,111,1111
Challenge 15 (String Length)        PASS    9 codes + 0 -> 9
Challenge 16 (Repeat Phrase)        PASS    echo "3"    -> HELLO x3
Challenge 17 (Palindrome)           PASS    echo "1221" -> YES
Challenge 18 (Collatz Steps)        PASS    echo "6"    -> 8
Challenge 19 (Run-Length Decode)    PASS    3,65,2,66.. -> decoded
Challenge 20 (Mini Gradebook)       PASS    12,8,15,10,14 -> 8,15,11
Challenge 21 (Recursive Fibonacci)  PASS    echo "7"    -> 13
Challenge 22 (Tiny VM)              PASS    PUSH 5,PRINT-> 5
Challenge 23 (Text Histogram)       PASS    2,4,1,3,5,2 -> labeled bars
Challenge 24 (Digital Clock Tick)   PASS    23:59:59    -> 0:0:0
Challenge 25 (Caesar Cipher)        PASS    shift 3,CODE-> 70,82,71,72
```

**25/25 PASS**

## License

These programs are released into the public domain. Do whatever you want with them. Arnold would approve.

> "I'll be back." -- to write more ArnoldC, probably.
