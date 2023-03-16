from . import BinOperator
from typing import Union
import z3


class Sub(BinOperator):
    @classmethod
    def get_name(cls) -> str:
        return "sub"

    @classmethod
    def get_id(cls) -> int:
        return 1

    @staticmethod
    def calc(
        x: Union[int, z3.ArithRef], y: Union[int, z3.ArithRef], *_
    ) -> Union[int, z3.ArithRef]:
        return x - y

    @classmethod
    def format(cls, target: dict) -> str:
        left, right = target["operands"][:2]
        res = f"%{left} - " if type(left) is int else f"({left}) - "
        res += f"%{right}" if type(right) is int else f"({right})"
        return res
