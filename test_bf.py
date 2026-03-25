#!/usr/bin/env python3
"""Test suite: ArnoldC Brainfuck interpreter vs reference brainfuck interpreter.

Runs BF programs through both interpreters and compares outputs.
The reference interpreter outputs raw bytes; the ArnoldC interpreter
outputs one integer per line. Comparison converts both to int lists.

Usage:
    python3 test_bf.py           # run all tests
    python3 test_bf.py -v        # verbose output
    python3 test_bf.py -k hello  # run tests matching 'hello'
"""

import dataclasses
import os
import subprocess
import sys
import tempfile
import time

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
ARNOLDC_JAR = os.path.join(PROJECT_DIR, "ArnoldC.jar")
BRAINFUCK_REF = "/opt/homebrew/bin/brainfuck"
TIMEOUT = 30

sys.path.insert(0, PROJECT_DIR)
from generate_bf_interpreter import generate, ENCODING


@dataclasses.dataclass
class TestCase:
    name: str
    bf_source: str
    description: str
    check_tape: dict = dataclasses.field(default_factory=dict)
    check_dp: int = None
    skip: str = ""  # reason to skip, empty = don't skip


# ============================================================
# TEST SUITE
# ============================================================

TEST_SUITE = [
    # --- Category 1: Trivial ---
    TestCase(
        name="empty_program",
        bf_source="",
        description="Empty program produces no output",
    ),
    TestCase(
        name="print_zero",
        bf_source=".",
        description="Print uninitialized cell (value 0)",
    ),
    TestCase(
        name="single_inc_print",
        bf_source="+.",
        description="Increment once and print (value 1)",
        check_tape={0: 1},
        check_dp=0,
    ),
    TestCase(
        name="five_incs",
        bf_source="+++++.",
        description="Increment 5 times and print (value 5)",
        check_tape={0: 5},
    ),
    TestCase(
        name="inc_dec",
        bf_source="+++--.",
        description="3 increments, 2 decrements -> print 1",
        check_tape={0: 1},
    ),

    # --- Category 2: Pointer movement ---
    TestCase(
        name="move_right_print",
        bf_source="+>++>+++.",
        description="Set 3 cells, print last (value 3)",
        check_tape={0: 1, 1: 2, 2: 3},
        check_dp=2,
    ),
    TestCase(
        name="move_left_print",
        bf_source="++>+++<.",
        description="Move right then left, print cell 0 (value 2)",
        check_dp=0,
    ),
    TestCase(
        name="multi_cell_print",
        bf_source="+++.>+++++.>+++++++.",
        description="Print 3 values from 3 cells: 3, 5, 7",
    ),
    TestCase(
        name="zigzag_print",
        bf_source="++>+++.<.>.",
        description="Zigzag: print cell1=3, cell0=2, cell1=3",
    ),

    # --- Category 3: Simple loops ---
    TestCase(
        name="multiply_3x2",
        bf_source="+++[>++<-]>.",
        description="Multiply 3*2=6 via loop",
        check_tape={0: 0, 1: 6},
    ),
    TestCase(
        name="add_3_5",
        bf_source="+++>+++++[<+>-]<.",
        description="Add 3+5=8 by moving cell1 into cell0",
        check_tape={0: 8, 1: 0},
    ),
    TestCase(
        name="clear_cell",
        bf_source="+++++[-].",
        description="Set to 5 then clear to 0 via [-]",
        check_tape={0: 0},
    ),
    TestCase(
        name="skip_loop_zero",
        bf_source="[+++].",
        description="Loop body skipped because cell is 0",
        check_tape={0: 0},
    ),
    TestCase(
        name="countdown_print",
        bf_source="++++[.-]",
        description="Print 4,3,2,1 via decrementing loop",
    ),
    TestCase(
        name="double_loop",
        bf_source="+++[-]++[-].",
        description="Two sequential loops, print 0 at end",
    ),

    # --- Category 4: Nested loops ---
    TestCase(
        name="nested_2x2x2",
        bf_source="++[>++[>++<-]<-]>>.",
        description="Nested multiply 2*2*2=8",
        check_tape={2: 8},
    ),
    TestCase(
        name="nested_3x3x3",
        bf_source="+++[>+++[>+++<-]<-]>>.",
        description="Nested multiply 3*3*3=27",
        check_tape={2: 27},
    ),
    TestCase(
        name="multiply_4x7",
        bf_source="++++[>+++++++<-]>.",
        description="4*7=28 via loop",
        check_tape={0: 0, 1: 28},
    ),
    TestCase(
        name="multiply_5x2",
        bf_source="+++++[>++<-]>.",
        description="5*2=10 via loop",
    ),

    # --- Category 5: ASCII character output ---
    TestCase(
        name="print_A",
        bf_source="++++++++[>++++++++<-]>+.",
        description="Print ASCII 65 = 'A'",
    ),
    TestCase(
        name="print_zero_char",
        bf_source="++++++[>++++++++<-]>.",
        description="Print ASCII 48 = '0'",
    ),
    TestCase(
        name="print_newline",
        bf_source="++++++++++.",
        description="Print ASCII 10 = newline",
    ),

    # --- Category 6: Edge cases ---
    TestCase(
        name="only_moves",
        bf_source=">>><<<",
        description="Only pointer moves, no output",
        check_dp=0,
    ),
    TestCase(
        name="loop_at_start_skip",
        bf_source="[>+<-]>.",
        description="Loop at start with cell=0, skipped entirely",
        check_tape={0: 0, 1: 0},
    ),
    TestCase(
        name="nested_skip",
        bf_source="[+[+[+]]].",
        description="Deeply nested brackets all skipped",
        check_tape={0: 0},
    ),
    TestCase(
        name="back_to_back_loops",
        bf_source="+++[-]++[>+++<-]>.",
        description="Clear then multiply: 2*3=6",
        check_tape={1: 6},
    ),

    # --- Category 7: Real-world programs ---
    TestCase(
        name="hello_world",
        bf_source=(
            "++++++++++[>+++++++>++++++++++>+++>+<<<<-]"
            ">++.>+.+++++++..+++.>++."
            "<<+++++++++++++++.>.+++.------.--------.>+.>."
        ),
        description="Classic Hello World (Daniel B. Cristofani variant)",
    ),
    TestCase(
        name="add_digits",
        bf_source=(
            "++++++[>++++++++<-]>"   # cell1 = 48 ('0')
            "+++++."                  # print '5' (48+5=53)
            "+."                      # print '6' (54)
            "+."                      # print '7' (55)
        ),
        description="Print ASCII digits 5, 6, 7",
    ),
    TestCase(
        name="alphabet_ABC",
        bf_source=(
            "++++++++[>++++++++<-]>+."  # 'A' = 65
            "+."                         # 'B' = 66
            "+."                         # 'C' = 67
        ),
        description="Print A, B, C as ASCII codes",
    ),
    TestCase(
        name="multiply_6x7_print",
        bf_source="++++++[>+++++++<-]>.",
        description="6*7=42, print ASCII '*'",
    ),
    TestCase(
        name="squares_1_to_5",
        bf_source=(
            # Compute n^2 for n=1..5 using n*n pattern
            # 1^2: just set to 1
            "+."
            # 2^2: add 3 (1+3=4)
            "+++."
            # 3^2: add 5 (4+5=9)
            "+++++."
            # 4^2: add 7 (9+7=16)
            "+++++++."
            # 5^2: add 9 (16+9=25)
            "+++++++++."
        ),
        description="Print squares 1,4,9,16,25 via successive odd number addition",
    ),
    TestCase(
        name="cell_copy",
        bf_source=(
            "+++++++++"                # cell0 = 9
            "[>+>+<<-]"               # copy cell0 to cell1 and cell2
            ">>[-<<+>>]"              # move cell2 back to cell0
            "<."                       # print cell1 (should be 9)
            "<."                       # print cell0 (should be 9)
        ),
        description="Copy cell0=9 to cell1, restore cell0, print both",
        check_tape={0: 9, 1: 9, 2: 0},
    ),
    TestCase(
        name="print_ABCDEFG",
        bf_source=(
            "++++++++[>++++++++<-]>+"  # cell0 = 65 ('A')
            ".+.+.+.+.+.+"            # print A(65) B(66) C(67) D(68) E(69) F(70) G(71)
        ),
        description="Print ASCII codes for ABCDEFG (65-71)",
    ),
    TestCase(
        name="powers_of_2",
        bf_source=(
            "+"                # cell0 = 1
            "."                # print 1
            "[>++<-]>."        # double to cell1=2, print
            "[>++<-]>."        # double to cell2=4, print
            "[>++<-]>."        # double to cell3=8, print
            "[>++<-]>."        # double to cell4=16, print
            "[>++<-]>."        # double to cell5=32, print
        ),
        description="Print powers of 2: 1, 2, 4, 8, 16, 32",
    ),
    TestCase(
        name="double_value",
        bf_source=(
            "+++++++++"            # cell0 = 9
            "[>++<-]"              # cell1 = 18, cell0 = 0
            ">."                   # print cell1 = 18
        ),
        description="Double 9 via loop: 9*2=18",
        check_tape={0: 0, 1: 18},
    ),

    # --- Category 8: Tape state verification (no output) ---
    TestCase(
        name="tape_setup_4_cells",
        bf_source="+>++>+++>++++",
        description="Set cells 0-3 to 1,2,3,4",
        check_tape={0: 1, 1: 2, 2: 3, 3: 4},
        check_dp=3,
    ),
    TestCase(
        name="tape_after_loop",
        bf_source="+++[>++<-]",
        description="After multiply loop: cell0=0, cell1=6",
        check_tape={0: 0, 1: 6},
        check_dp=0,
    ),
    TestCase(
        name="tape_swap",
        bf_source=(
            "+++++>+++"           # cell0=5, cell1=3
            "[<+>-]"              # add cell1 to cell0, cell1=0
        ),
        description="Move cell1 into cell0: cell0=8, cell1=0",
        check_tape={0: 8, 1: 0},
        check_dp=1,
    ),
]


# ============================================================
# TEST RUNNER
# ============================================================

@dataclasses.dataclass
class TestResult:
    name: str
    status: str  # PASS, FAIL, ERROR, SKIP
    duration: float = 0.0
    arnoldc_output: list = dataclasses.field(default_factory=list)
    reference_output: list = dataclasses.field(default_factory=list)
    tape: list = dataclasses.field(default_factory=list)
    dp: int = -1
    message: str = ""


class BFTestRunner:
    def __init__(self, work_dir, verbose=False):
        self.work_dir = work_dir
        self.verbose = verbose

    def run_reference(self, bf_source):
        """Run BF program with reference interpreter, return list of byte values."""
        if not bf_source:
            return []
        result = subprocess.run(
            [BRAINFUCK_REF, "-e", bf_source],
            capture_output=True, timeout=TIMEOUT,
        )
        return list(result.stdout)

    def run_arnoldc(self, bf_source):
        """Generate, compile, run ArnoldC BF interpreter. Returns (output_ints, tape, dp)."""
        safe_name = "bf_test"
        arnoldc_path = os.path.join(self.work_dir, f"{safe_name}.arnoldc")

        generate(bf_source, output_path=arnoldc_path)

        # Compile (must run from work_dir so class name is simple)
        comp = subprocess.run(
            ["java", "-jar", ARNOLDC_JAR, f"{safe_name}.arnoldc"],
            capture_output=True, text=True, timeout=TIMEOUT,
            cwd=self.work_dir,
        )
        if comp.returncode != 0:
            raise RuntimeError(f"Compilation failed:\n{comp.stderr}")

        # Run
        run = subprocess.run(
            ["java", safe_name],
            capture_output=True, text=True, timeout=TIMEOUT,
            cwd=self.work_dir,
        )
        if run.returncode != 0:
            raise RuntimeError(f"Execution failed:\n{run.stderr}")

        return self._parse_arnoldc_output(run.stdout)

    def _parse_arnoldc_output(self, stdout):
        """Parse ArnoldC output into (output_ints, tape_cells, dp)."""
        lines = stdout.strip().split("\n")

        try:
            sep_idx = lines.index("---")
        except ValueError:
            # No separator — treat all lines as output
            output_ints = [int(l) for l in lines if l.strip()]
            return output_ints, [], -1

        output_lines = lines[:sep_idx]
        output_ints = [int(l) for l in output_lines if l.strip()]

        meta = lines[sep_idx + 1:]
        tape_start = meta.index("TAPE") + 1
        dp_idx = meta.index("DP")
        tape = [int(meta[i]) for i in range(tape_start, dp_idx)]
        dp = int(meta[dp_idx + 1])

        return output_ints, tape, dp

    def compare_outputs(self, arnoldc_out, reference_out):
        """Compare outputs, applying %256 normalization to ArnoldC values."""
        a = [v % 256 for v in arnoldc_out]
        r = reference_out
        if a == r:
            return True, ""

        diffs = []
        max_len = max(len(a), len(r))
        for i in range(min(max_len, 20)):  # show at most 20 diffs
            av = a[i] if i < len(a) else "<missing>"
            rv = r[i] if i < len(r) else "<missing>"
            if av != rv:
                rv_chr = chr(rv) if isinstance(rv, int) and 32 <= rv < 127 else ""
                diffs.append(f"  [{i}] arnoldc={av} ref={rv}{' ' + repr(rv_chr) if rv_chr else ''}")
        if len(a) != len(r):
            diffs.append(f"  lengths differ: arnoldc={len(a)} ref={len(r)}")
        return False, "\n".join(diffs)

    def check_tape_state(self, tape, dp, tc):
        """Verify tape cells and dp against test case expectations."""
        issues = []
        for idx, expected in tc.check_tape.items():
            if idx < len(tape):
                actual = tape[idx]
                if actual != expected:
                    issues.append(f"  tape[{idx}]: expected={expected} actual={actual}")
            else:
                issues.append(f"  tape[{idx}]: out of range (tape has {len(tape)} cells)")
        if tc.check_dp is not None and dp != tc.check_dp:
            issues.append(f"  dp: expected={tc.check_dp} actual={dp}")
        return issues

    def run_test(self, tc):
        """Run a single test case."""
        if tc.skip:
            return TestResult(name=tc.name, status="SKIP", message=tc.skip)

        start = time.time()
        try:
            ref_out = self.run_reference(tc.bf_source)
            a_out, tape, dp = self.run_arnoldc(tc.bf_source)
            duration = time.time() - start

            match, diff_msg = self.compare_outputs(a_out, ref_out)

            result = TestResult(
                name=tc.name, status="PASS" if match else "FAIL",
                duration=duration,
                arnoldc_output=a_out, reference_output=ref_out,
                tape=tape, dp=dp,
            )

            if not match:
                result.message = f"Output mismatch:\n{diff_msg}"
                return result

            # Check tape state if specified
            tape_issues = self.check_tape_state(tape, dp, tc)
            if tape_issues:
                result.status = "FAIL"
                result.message = "Tape state mismatch:\n" + "\n".join(tape_issues)

            return result

        except subprocess.TimeoutExpired:
            return TestResult(
                name=tc.name, status="ERROR",
                duration=time.time() - start,
                message="Timeout (possible infinite loop)",
            )
        except Exception as e:
            return TestResult(
                name=tc.name, status="ERROR",
                duration=time.time() - start,
                message=str(e),
            )

    def run_all(self, filter_pattern=""):
        """Run all test cases, optionally filtered by name pattern."""
        results = []
        cases = TEST_SUITE
        if filter_pattern:
            cases = [tc for tc in cases if filter_pattern.lower() in tc.name.lower()]

        print(f"{'=' * 60}")
        print(f"BF Interpreter Test Suite ({len(cases)} tests)")
        print(f"{'=' * 60}")
        print()

        for tc in cases:
            result = self.run_test(tc)
            results.append(result)
            self._print_result(result, tc)

        self._print_summary(results)
        return results

    def _print_result(self, result, tc):
        """Print a single test result."""
        status_icon = {
            "PASS": "\033[32m[PASS]\033[0m",
            "FAIL": "\033[31m[FAIL]\033[0m",
            "ERROR": "\033[31m[ERR ]\033[0m",
            "SKIP": "\033[33m[SKIP]\033[0m",
        }
        icon = status_icon.get(result.status, "[????]")
        timing = f"({result.duration:.2f}s)" if result.duration > 0 else ""
        print(f"  {icon} {result.name:<30s} {timing}")

        if self.verbose and result.status == "PASS":
            if result.arnoldc_output:
                chars = "".join(chr(v % 256) if 32 <= (v % 256) < 127 else "." for v in result.arnoldc_output)
                print(f"         output: {result.arnoldc_output[:10]}{'...' if len(result.arnoldc_output) > 10 else ''} = \"{chars}\"")

        if result.message:
            for line in result.message.split("\n"):
                print(f"         {line}")

    def _print_summary(self, results):
        """Print test summary."""
        passed = sum(1 for r in results if r.status == "PASS")
        failed = sum(1 for r in results if r.status == "FAIL")
        errors = sum(1 for r in results if r.status == "ERROR")
        skipped = sum(1 for r in results if r.status == "SKIP")
        total_time = sum(r.duration for r in results)

        print()
        print(f"{'=' * 60}")
        color = "\033[32m" if failed == 0 and errors == 0 else "\033[31m"
        print(f"{color}Results: {passed} passed, {failed} failed, "
              f"{errors} errors, {skipped} skipped\033[0m")
        print(f"Total time: {total_time:.1f}s")
        print(f"{'=' * 60}")


def main():
    verbose = "-v" in sys.argv
    filter_pattern = ""
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "-k" and i < len(sys.argv) - 1:
            filter_pattern = sys.argv[i + 1]
        elif arg.startswith("-k"):
            filter_pattern = arg[2:]

    with tempfile.TemporaryDirectory(prefix="bf_test_") as tmpdir:
        runner = BFTestRunner(tmpdir, verbose=verbose)
        results = runner.run_all(filter_pattern)
        failures = sum(1 for r in results if r.status in ("FAIL", "ERROR"))
        sys.exit(1 if failures > 0 else 0)


if __name__ == "__main__":
    main()
