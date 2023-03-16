from pukeko.operators import factory


def test_id():
    assert factory.create("xor").get_id() == 4
    assert factory.create("xor").get_name() == "xor"


def test_calc():
    assert factory.create("xor").calc(1, 5) == 4
