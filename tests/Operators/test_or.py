from pukeko.operators import factory


def test_id():
    assert factory.create("or").get_id() == 2
    assert factory.create("or").get_name() == "or"


def test_calc():
    assert factory.create("or").calc(1, 4) == 5
