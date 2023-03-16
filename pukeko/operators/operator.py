from abc import (
    ABC,
    abstractclassmethod,
    abstractmethod,
    abstractclassmethod,
    abstractstaticmethod,
)
from pukeko.values import Values
from typing import Union
import z3


class Operator(ABC):
    @abstractclassmethod
    def get_id(cls) -> int:
        pass

    @abstractclassmethod
    def get_name(cls) -> str:
        pass

    @abstractstaticmethod
    def calc() -> Union[int, z3.ArithRef]:
        pass

    @abstractmethod
    def get_const(self, values: Values, idx: int, opcode: z3.BitVecRef) -> list:
        pass

    # オペランドの参照を返す（不要な命令の生成防止制約を実装するために用いる）
    @classmethod
    def get_operands(
        cls, opcode: z3.BitVecRef, target_operand: int, operands: list[z3.BitVecRef]
    ):
        return z3.And(
            opcode == cls.get_id(),
            z3.Or(
                [
                    operand == target_operand
                    for operand in operands[: len(cls.get_init_values())]
                ]
            ),
        )

    @abstractclassmethod
    def get_const_with_prohibited_inst(self, inst: dict, opcode: z3.BitVecRef) -> list:
        pass

    @abstractstaticmethod
    def get_init_values(self) -> list[int]:
        pass

    @abstractmethod
    def eval(self, model: z3.ModelRef) -> dict:
        pass

    @abstractclassmethod
    def format(cls, target: dict, prefix: str = "", brancket: bool = False) -> str:
        pass
