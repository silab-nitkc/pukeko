from typing import Optional
from uuid import uuid4
from pukeko.operators import factory
import z3


class Instruction:
    def __init__(
        self,
        index: int,
        insert_after: Optional["Instruction"] = None,
        num_io_examples: int = 20,
    ):
        self.insert_after(insert_after)
        self.opcode = z3.BitVec(f"op{index}: " + str(uuid4()), 8)
        self.operands = [
            z3.BitVec(f"operand{index}-{i}" + str(uuid4()), 8) for i in range(3)
        ]
        self.init_values = []
        self.init_values_with_int = []
        self.index = index
        self.res_value_with_int = []
        self.res_value = [
            z3.BitVec(f"resVal{index}: {uuid4()}", 8) for _ in range(num_io_examples)
        ]

    def insert_after(self, parent: "Instruction"):
        self.parent = parent

    def set_init_values(self, init_values: list[list[int]]):
        self.init_values_with_int = init_values
        self.init_values = []
        for values in init_values:
            self.init_values += [
                [
                    z3.BitVec(f"val{self.index}-{i}: {uuid4()}", 8)
                    for i in range(len(values))
                ]
            ]

    def get_values(self, pattern_index: int) -> list[z3.BitVecRef]:
        if self.parent is None:
            if pattern_index >= len(self.init_values):
                return []
            return [*self.init_values[pattern_index]]
        return [
            *self.parent.get_values(pattern_index),
            self.parent.res_value[pattern_index],
        ]

    def get_value_at(self, pattern_index: int, index: int) -> z3.BitVecRef:
        values = self.get_values(pattern_index)
        res = True
        for i, value in enumerate(values):
            res = z3.If(index == i, value, res)
        return res

    def set_result(self, values: list[int]):
        self.res_value_with_int = values

    def get_opcodes(self):
        if self.parent is None:
            return [self.opcode]
        return [*self.parent.get_opcodes(), self.opcode]

    def get_operands(self):
        if self.parent is None:
            return [self.operands]
        return [*self.parent.get_operands(), self.operands]

    def get_const(self) -> list:
        const_list = []
        for op in factory.all():
            const_list += op().get_const(
                self.get_opcodes(),
                self.res_value,
                [
                    [self.get_value_at(i, operand) for operand in self.operands]
                    for i in range(len(self.res_value))
                ],
                self.get_operands(),
                len(self.get_values(0)),
                [self.get_values(i) for i in range(len(self.res_value))],
            )
        const_list += [
            z3.ULT(self.opcode, len(factory.all())),
        ]

        for z3values, values in zip(self.init_values, self.init_values_with_int):
            const_list += [
                z3val == val for z3val, val in zip(z3values, values) if val is not None
            ]

        for z3value, value in zip(self.res_value, self.res_value_with_int):
            const_list += [z3value == value]

        # 同じ命令の連続利用を禁止
        if self.parent:
            const_list += [self.opcode != self.parent.opcode]

        return const_list

    def get_const_with_prohibited_instseq(self, target: dict) -> list:
        """与えられた命令列を再生成しないようにする制約を返す"""
        const_list = []
        for op in factory.all():
            const_list += op.get_const_with_prohibited_inst(
                target, self.opcode, self.operands
            )
        return const_list

    def eval(self, model: z3.ModelRef) -> list:
        opcode = model.eval(self.opcode).as_long()
        op = next(filter(lambda x: x.get_id() == opcode, factory.all()))
        return {
            **op().eval(model, *self.operands),
            "init_num": len(self.init_values_with_int[0])
            if len(self.init_values_with_int)
            else 0,
        }
