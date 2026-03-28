# Chessboard Demo: ArnoldC interprets Brainfuck rendering a chess position

A 1,092-instruction Brainfuck program ([chessboard.b](https://brainfuck.org/chessboard.b) by Daniel B. Cristofani) reads a FEN string and renders an ASCII art chessboard. It runs through `bf_vm_chess.arnoldc` — a 23,292-line ArnoldC Brainfuck interpreter.

This was previously listed as "impossible" (program too large, uses interactive input). Both blockers were resolved: configurable program size (`--prog 1100`) and BF input (`,`) reading from stdin after the program data.

## Quick Start

```bash
# Compile once:
java -jar ../../ArnoldC-patched.jar bf_vm_chess.arnoldc

# Starting position:
./run.sh

# Custom FEN:
./run.sh "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR"
```

## Example Positions

### Starting position
```
./run.sh
```
```
+-------+-------+-------+-------+-------+-------+-------+-------+
| [_|_] |::_,/|:|  /\   |::\|/::|  \+/  |::/\::|  _,/| |:[_|_]:|
|  [#]  |:/_#)\:|  \#/  |::(#)::|  {#}  |::\#/::| /_#)\ |::[#]::|
|  [#]  |::/#\\:|  (#)  |::(#)::|  {#}  |::(#)::|  /#\  |::[#]::|
| (###) |:(###):| (###) |:(###):| (###) |:(###):| (###) |:(###):|
+-------+-------+-------+-------+-------+-------+-------+-------+
```

### Sicilian Defense (1.e4 c5)
```
./run.sh "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR"
```
The c5 pawn and e4 pawn are visible on the board.

### Scholar's Mate setup
```
./run.sh "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR"
```
White's queen on h5 and bishop on c4 are targeting f7.

## How it works

```
FEN string           BF program            ArnoldC interpreter       Output
"rnbqkbnr/..."  ──▶  chessboard.b    ──▶   bf_vm_chess.arnoldc  ──▶  ASCII art
(44 ASCII codes)     (1,092 instr)         (23,292 lines)           chessboard
                     reads via ,            interprets BF from
                     17 input reads         stdin, all 8 opcodes
```

The input protocol packs everything into one stdin stream:
1. Program length (1092)
2. Encoded BF instructions (1092 integers: +=3, -=4, >=1, etc.)
3. FEN string as ASCII codes (e.g., 114 110 98 113 ... 10)

The shared Scanner reads them sequentially — program data first, then the BF `,` instructions consume the FEN characters during execution.

## What's in this folder

| File | Lines | Description |
|------|------:|-------------|
| `chessboard.b` | — | Original BF source from [brainfuck.org](https://brainfuck.org/chessboard.b) |
| `bf_vm_chess.arnoldc` | 23,292 | ArnoldC BF interpreter sized for chessboard (--prog 1100 --tape 50) |
| `run.sh` | — | Helper script: encodes FEN + BF, pipes to ArnoldC, decodes output |

## Performance

| Metric | Value |
|--------|-------|
| BF instructions | 1,092 |
| BF execution steps | 305,830 |
| BF input reads (`,`) | 17 |
| Output characters | 2,376 |
| Tape cells used | 37 |
| ArnoldC execution time | ~4.3 seconds |

## Regenerating

```bash
python3 ../../build_bf_vm.py bf_vm_chess.arnoldc --prog 1100 --tape 50
java -jar ../../ArnoldC-patched.jar bf_vm_chess.arnoldc
```
