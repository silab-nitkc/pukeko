from pukeko.operators import factory


def test_id():
    assert factory.create("and").get_id() == 3
    assert factory.create("and").get_name() == "and"


def test_calc():
    assert factory.create("and").calc(1, 5) == 1
