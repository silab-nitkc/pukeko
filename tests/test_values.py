from pukeko.values import Values


def test_init():
    values = Values(5)
    assert len(values.registers) == 5
    assert len(values.init_values) == 5


def test_set_init_values():
    values = Values(5)
    values.set_init_value(2, [1, 2])
    assert values.init_values[0] == []
    assert values.init_values[2] == [1, 2]


def test_get():
    values = Values(2)
    assert values.get(0) == [values.registers[0][0], values.registers[1][0]]


def test_get_init_registers():
    values = Values(5)
    values.set_init_value(2, [1, 2])
    assert values.get_init_registers(0) == []
    assert values.get_init_registers(2) == [
        values.registers[2][0],
        values.registers[2][1],
    ]


def test_get_values_with_offset():
    values = Values(1)
    values.set_init_value(0, [1, 2])
    assert values.get_values_with_offset(0) == [
        values.registers[0][2],
    ]


def test_get_offset():
    values = Values(5)
    values.set_init_value(2, [1, None])
    assert values.get_offset(0) == 0
    assert values.get_offset(2) == 2


def test_get_const():
    values = Values(2)
    values.set_init_value(0, [1, None])
    const_list = values.get_const()
    assert (values.registers[0][0] == 1) in const_list
    assert (values.registers[0][1] == 2) not in const_list
