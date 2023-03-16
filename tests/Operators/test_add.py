from pukeko.operators import factory


def test_id():
    assert factory.create("add").get_id() == 0
    assert factory.create("add").get_name() == "add"


def test_calc():
    assert factory.create("add").calc(1, 2) == 3
