from typing import Optional
import z3
from random import randint
from .. import ConfigLoader

from . import Operator


class BinOperator(Operator):
    def __init__(self) -> None:
        pass

    def get_const(
        self,
        opcodes: list[z3.BitVecRef],
        res_values: list[z3.BitVecRef],
        values: list[list[z3.BitVecRef]],
        operands: list[list[z3.BitVecRef]],
        res_index: int,
        all_values: Optional[list[list[z3.BitVecRef]]] = [],
    ) -> list:
        const_list = []
        const_list += [
            res == self.calc(*values) for res, values in zip(res_values, values)
        ]
        const_list += [
            z3.ULT(operands[-1][0], res_index),
            z3.ULT(operands[-1][1], res_index),
        ]
        if self.get_name() not in ConfigLoader.config["outputOperators"]:
            const_list += [False]

        const_list += [operands[-1][0] != operands[-1][1]]
        return [
            z3.If(
                opcodes[-1] == self.get_id(),
                z3.And(const_list),
                True,
            )
        ]

    @classmethod
    def get_const_with_prohibited_inst(
        cls, inst: dict, opcode: z3.BitVecRef, operands: list[z3.BitVecRef]
    ) -> list:
        """与えられた命令列を再生成しないようにする制約を返す"""

        if cls.get_name() != inst["name"]:
            return []

        const_list = []
        const_list += [
            z3operand != int(operand)
            for z3operand, operand in zip(operands, inst["operands"])
        ]
        const_list += [opcode != cls.get_id()]

        return const_list

    @staticmethod
    def get_init_values() -> list[int]:
        return [randint(0, 255), randint(0, 255)]

    def eval(self, model: z3.ModelRef, left: z3.BitVecRef, right: z3.BitVecRef, *_):
        return {
            "name": self.get_name(),
            "operands": [model.eval(left).as_long(), model.eval(right).as_long()],
        }
