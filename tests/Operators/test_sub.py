from pukeko.operators import factory


def test_id():
    assert factory.create("sub").get_id() == 1
    assert factory.create("sub").get_name() == "sub"


def test_calc():
    assert factory.create("sub").calc(1, 2) == -1
