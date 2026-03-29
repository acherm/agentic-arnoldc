#!/bin/bash
# True triple chain with BF input: ArnoldC → MnM → BF (,)
#
# NO PYTHON AT RUNTIME. Pure shell + Java.
#
# BF program: ,>,<[>[>+>+<<-]>>[<<+>>-]<<<-]>>.
#   Reads two integers via , (BF input), multiplies them, prints result.
#
# The MnM BF interpreter is pre-computed in stdin_base.txt.
# This script appends the BF input values and pipes to mnm_vm.
#
# Usage:
#   ./run.sh 6 7       # prints 42 (6 × 7)
#   ./run.sh 12 11     # prints 132 (12 × 11)
#   ./run.sh 3 14      # prints 42 (3 × 14)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PATCHED_JAR="$SCRIPT_DIR/../../ArnoldC-patched.jar"

A="${1:-6}"
B="${2:-7}"

# Compile if needed
if [ ! -f "$SCRIPT_DIR/mnm_vm_multiply.class" ]; then
    echo "Compiling mnm_vm_multiply.arnoldc (51,337 lines)..." >&2
    cd "$SCRIPT_DIR" && java -jar "$PATCHED_JAR" mnm_vm_multiply.arnoldc
fi

# Feed: pre-computed MnM program + variable inits, then 2 input values
{
    cat "$SCRIPT_DIR/stdin_base.txt"
    echo 2        # numInputs = 2
    echo "$A"     # first BF , reads this
    echo "$B"     # second BF , reads this
} | java -cp "$SCRIPT_DIR" mnm_vm_multiply 2>&1
