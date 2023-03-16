from ..operators import factory
from . import Presentor
import json


class PrintFormula(Presentor):
    def __init__(self) -> None:
        self.last_output = ""

    def run(self, target: list[dict]) -> None:
        self.last_output = self._format_as_formula(target)
        print(self.last_output, flush=True)

    def start(self) -> None:
        pass

    def push(self, target: dict) -> None:
        self.run(target)

    def end(self) -> None:
        pass

    def get_last_output(self) -> str:
        return self.last_output

    def _format_as_formula(self, target: list[dict], index: int = -1) -> str:
        offset = target[0]["init_num"]
        if index == 0:
            return factory.create(target[index]["name"]).format(target[index])

        return factory.create(target[index]["name"]).format(
            {
                "name": target[index]["name"],
                "operands": [
                    self._format_as_formula(target, operand - offset)
                    if type(operand) is int and operand >= offset
                    else operand
                    for operand in target[index]["operands"]
                ],
            }
        )

    def _count_init_values(self, target: dict) -> int:
        keys = ["left", "right"]
        filtered = {key: value for key, value in target.items() if key in keys}

        return max(filtered.values())
