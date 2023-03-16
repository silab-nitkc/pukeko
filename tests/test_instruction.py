from pukeko.instruction import Instruction


def test_get_values():
    inst_a = Instruction(0)
    inst_a.set_init_values([[1, 2]])
    inst_b = Instruction(1, inst_a)

    assert [
        *inst_a.init_values[0][:2],
        inst_a.res_value[0],
    ] == inst_b.get_values(0)
