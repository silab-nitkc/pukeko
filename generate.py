#!/usr/bin/python3
"""Overview:
    Generates a code fragment that satisfy the specified conditions.

Usage:
    generate <opname> [-l <L>] [-a] [-f]

Options:
    opname  : Name of target instruction (add, sub, or, and, xor)
    -l <L>  : Length of instruction sequence to be generated [default: 10]
    -f      : Output formulas
    -a      : (Experimental) Generate all possible instruction sequences
"""


from docopt import docopt
from pukeko.controllers import PukekoController
from pukeko.presentors import PrintFormula, PrintJson
from pukeko.ConfigLoader import load

if __name__ == "__main__":
    MAX_N = 100000
    args = docopt(__doc__)

    generator = PukekoController(PrintFormula() if args["-f"] else PrintJson())
    load()
    generator.generate_inst_seq(
        int(args["-l"]), args["<opname>"], MAX_N if args["-a"] else 1
    )
