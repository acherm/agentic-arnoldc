#!/bin/bash
# Run chessboard.b through bf_vm — ArnoldC interprets Brainfuck
#
# Usage:
#   ./run.sh                                          # default starting position
#   ./run.sh "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"  # explicit FEN
#   ./run.sh "r1bqkb1r/pppppppp/2n2n2/8/4P3/8/PPPP1PPP/RNBQKBNR"  # after 1.e4 Nc6 2.Nf3

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PATCHED_JAR="$SCRIPT_DIR/../../ArnoldC-patched.jar"

# Default: standard starting position (full FEN with all 6 fields required)
FEN="${1:-rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1}"

# Compile if needed
if [ ! -f "$SCRIPT_DIR/bf_vm_chess.class" ]; then
    echo "Compiling bf_vm_chess.arnoldc..."
    cd "$SCRIPT_DIR" && java -jar "$PATCHED_JAR" bf_vm_chess.arnoldc
fi

# Encode BF program + FEN input
python3 -c "
import sys
with open('$SCRIPT_DIR/chessboard.b') as f: src = f.read()
enc = {'>':1,'<':2,'+':3,'-':4,'.':5,',':6,'[':7,']':8}
codes = [enc[c] for c in src if c in enc]
fen = sys.argv[1]
fen_codes = [ord(c) for c in fen] + [10]  # newline-terminated
print(len(codes), ' '.join(str(c) for c in codes), ' '.join(str(c) for c in fen_codes))
" "$FEN" | java -cp "$SCRIPT_DIR" bf_vm_chess 2>&1 | python3 -c "
import sys
vals = [int(l.strip()) for l in sys.stdin if l.strip()]
# ArnoldC uses 32-bit signed ints; BF expects 8-bit unsigned.
# Map to 0-255 range, then to characters.
# Box-drawing: 252='+' 254='-' (replacing extended ASCII with ASCII equivalents)
REMAP = {252: ord('+'), 254: ord('-'), -4: ord('+'), -2: ord('-')}
chars = []
for v in vals:
    v = REMAP.get(v, v % 256 if v < 0 else v)
    if 0 <= v < 128:
        chars.append(chr(v))
    else:
        chars.append(chr(v % 256) if 32 <= v % 256 < 127 else '+')
print(''.join(chars))
"
