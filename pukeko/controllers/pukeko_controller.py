from pukeko.interactors import GenerateInstSeq
from pukeko.presentors import Presentor, PrintJson
from pukeko.operators import factory
from pukeko import ConfigLoader


class PukekoController:
    def __init__(self, presentor: Presentor = PrintJson()) -> None:
        self.presentor = presentor

    def generate_inst_seq(self, length: int, opname: str, N: int = 1) -> None:
        if opname not in ConfigLoader.config["targetOperators"]:
            return

        interactor = GenerateInstSeq(self.presentor)
        original = {
            "name": opname,
            "operands": [
                i for i in range(len(factory.create(opname).get_init_values()))
            ],
            "init_num": len(factory.create(opname).get_init_values())
        }

        interactor.generate_inst_seq(length, original, N=N)
