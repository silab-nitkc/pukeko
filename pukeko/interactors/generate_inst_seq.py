from pukeko.instruction import Instruction
from pukeko.operators import factory
from pukeko.presentors import Presentor, PrintJson
from pukeko import ConfigLoader
import z3


class GenerateInstSeq:
    def __init__(self, presentor: Presentor = PrintJson()):
        self.presentor = presentor

    def generate_inst_seq(
        self, length: int, target: dict, num_io_examples: int = 5, N: int = 1
    ) -> None:
        instructions = [
            Instruction(i, num_io_examples=num_io_examples) for i in range(length)
        ]
        for parent, child in zip(instructions, instructions[1:]):
            child.insert_after(parent)

        target_op = factory.create(target["name"])()
        init_values = [target_op.get_init_values() for i in range(num_io_examples)]
        instructions[0].set_init_values(init_values)
        instructions[-1].set_result(
            map(lambda args: target_op.calc(*args), init_values)
        )

        const_list = []
        for inst in instructions:
            const_list += inst.get_const()

        # 不要な命令が発生しないように制約を追加する
        # 「全てのオペランドは、必ず一度以上参照される」
        for operand_idx in range(len(instructions[-1].get_values(0))):
            distinct_const = []
            for inst in instructions:
                distinct_const += [
                    op.get_operands(inst.opcode, operand_idx, inst.operands)
                    for op in factory.all()
                ]
            const_list += [z3.Or(distinct_const)]

        # 「指定された命令は、最低1回は実行される」
        for op in [
            op
            for op in factory.all()
            if op.get_name() in ConfigLoader.config["atLeastOnce"]
        ]:
            const_list += [z3.Or([inst.opcode == op.get_id() for inst in instructions])]

        solver = z3.Solver()
        solver.add(const_list)

        generated_all = []

        if N > 1:
            self.presentor.start()

        while len(generated_all) < N:
            if solver.check() == z3.unsat:
                self.presentor.run([target])
                break

            model = solver.model()
            generated = [inst.eval(model) for inst in instructions]

            retry_const = []
            for inst, generated_inst in zip(instructions, generated):
                retry_const+=inst.get_const_with_prohibited_instseq(generated_inst)
            solver.add(z3.Or(retry_const))

            if not self.test(target, generated):
                continue

            generated_all += [generated]

            if N == 1:
                self.presentor.run(generated)
            else:
                self.presentor.push(generated)

        if N > 1:
            self.presentor.end()

    def test(self, original: dict, target_list: list[dict]) -> bool:
        length = len(target_list)
        const_list = []

        instructions = [Instruction(i, num_io_examples=1) for i in range(length)]
        instructions[0].set_init_values(
            [[None for _ in factory.create(original["name"]).get_init_values()]]
        )
        for parent, child in zip(instructions, instructions[1:]):
            child.insert_after(parent)

        original_op = factory.create(original["name"])()

        # 元来の命令の入出力制約を設定
        const_list += [
            instructions[-1].res_value[0]
            != original_op.calc(
                *[
                    instructions[0].get_value_at(0, int(operand))
                    for operand in original["operands"]
                ]
            )
        ]
        for inst, target in zip(instructions, target_list):
            const_list += inst.get_const()

            target_opcode = factory.create(target["name"]).get_id()
            const_list += [inst.opcode == target_opcode]
            for z3operand, operand in zip(inst.operands, target["operands"]):
                const_list += [z3operand == int(operand)]

        solver = z3.Solver()
        solver.add(const_list)
        return solver.check() == z3.unsat
