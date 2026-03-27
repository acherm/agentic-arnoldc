# Demos

Pre-built artifacts demonstrating ArnoldC interpreters at work. Each subfolder is self-contained with its own README.

| Demo | What it shows | Key artifact |
|------|--------------|-------------|
| [`triplechain/`](triplechain/) | **ArnoldC → MnM → Brainfuck** — three interpreters deep, including a true single-file interpreter that reads MnM from stdin | `mnm_vm_bf.arnoldc` (26,757 lines) |
| [`mnm-standalone/`](mnm-standalone/) | MnM programs (hello world, factorial, fizzbuzz) compiled to ArnoldC via the generator | `mnm_factorial.arnoldc` (1,979 lines) |
| [`mnm-compiler/`](mnm-compiler/) | Same MnM programs showing source + compiled output side by side | `factorial.mnm` → `mnm_factorial.arnoldc` |

All demos require the **patched ArnoldC compiler** (`ArnoldC-patched.jar` in the parent directory) for programs with >100 variables or using `static_fields` mode.
