# MnM Compiler: MnM → ArnoldC

MnM programs compiled to tailored ArnoldC by `generate_mnm_interpreter.py`. Each generated ArnoldC file is specific to the input MnM program — different inputs produce different ArnoldC code.

## Quick Start

```bash
# Compile and run factorial:
java -jar ../../ArnoldC-patched.jar mnm_factorial.arnoldc
java mnm_factorial
# Output: 120

# Compile and run hello world:
java -jar ../../ArnoldC-patched.jar mnm_hello_world.arnoldc
java mnm_hello_world
# Output: Hello, world!
```

## What's in this folder

| MnM source | ArnoldC output | Lines | Description |
|------------|---------------|------:|-------------|
| `hello_world.mnm` + `.json` | `mnm_hello_world.arnoldc` | 1,569 | Prints "Hello, world!" (uses PRINT_STR) |
| `factorial.mnm` + `.json` | `mnm_factorial.arnoldc` | 1,979 | Computes 5! = 120 (uses READ_INT) |

## Compiler vs True Interpreter

This demo shows the **compiler** approach. The generated ArnoldC is tailored to each input:
- Variable counts, stack sizes, and method signatures match the specific program
- Strings are hardcoded as `TALK TO THE HAND "..."` literals
- Input queue values are embedded in the code

For the **true interpreter** approach (a single fixed ArnoldC program that reads any MnM from stdin), see [`../mnm-standalone/`](../mnm-standalone/).

## Regenerating

```bash
python3 ../../generate_mnm_interpreter.py factorial.mnm factorial.mnm.json mnm_factorial.arnoldc --static-fields
python3 ../../generate_mnm_interpreter.py hello_world.mnm hello_world.mnm.json mnm_hello_world.arnoldc --static-fields
```
