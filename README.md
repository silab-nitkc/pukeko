# pukeko
*pukeko* is an experimental code fragment generator. Pukeko takes an operator name of assembly program, and returns an code fragment with the same semantics. The code fragments are generated using an SMT solver Z3.

### Example (`add` instruction):
```diff
  %1 = load i32, i32* %x, align 4
  %2 = load i32, i32* %x, align 4
- %3 = add i32 %1, %2
+ %3 = and i32 %1, %2
+ %4 = and i32 %3, %2
+ %5 = sub i32 %4, %3
+ %6 = and i32 %1, %5
+ %7 = and i32 %1, %6
+ %8 = or i32 %7, %6
+ %9 = sub i32 %8, %5
+ %10 = and i32 %1, %9
+ %11 = or i32 %10, %1
+ %12 = add i32 %11, %2
```

## Requirements
- Python 3.9 (or higher)
- z3py
- docopt

## Usage
```
Overview:
    Generates a code fragment that satisfy the specified conditions.

Usage:
    generate <opname> [-l <L>] [-a] [-f]

Options:
    opname  : Name of target instruction (add, sub, or, and, xor)
    -l <L>  : Length of instruction sequence to be generated [default: 5]
    -f      : Output formulas
    -a      : (Experimental) Generate all possible instruction sequences
```

### Example
```bash
python generate.py add -l 5 -f
```