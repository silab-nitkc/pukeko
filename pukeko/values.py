import z3
from uuid import uuid4


class Values:
    def __init__(self, num_examples: int) -> None:
        self.registers = [
            z3.Array(str(uuid4()), z3.BitVecSort(4), z3.BitVecSort(8))
            for i in range(num_examples)
        ]
        self.init_values = [[] for i in range(num_examples)]

    def set_init_value(self, idx: int, col_values: list[int]) -> None:
        self.init_values[idx] = col_values

    def get(self, idx: int) -> list[z3.BitVecRef]:
        return list(map(lambda col: col[idx], self.registers))

    def get_init_registers(self, idx: int) -> list[z3.BitVecRef]:
        target_register = self.registers[idx]
        init_value = self.init_values[idx]
        return [target_register[i] for i in range(len(init_value))]

    def get_values_with_offset(self, op_idx) -> z3.BitVecRef:
        return [
            reg[op_idx + len(self.init_values[i])]
            for i, reg in enumerate(self.registers)
        ]

    def get_offset(self, idx: int) -> int:
        return len(self.init_values[idx])

    def get_const(self) -> list:
        const_list = []

        for register, init_val in zip(self.registers, self.init_values):
            const_list += [
                reg == val for reg, val in zip(register, init_val) if val is not None
            ]

        return const_list
