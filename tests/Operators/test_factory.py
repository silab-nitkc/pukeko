from pukeko.operators import factory
from pukeko.operators import Add


def test_create_by_id():
    assert factory.createById(0) == Add


def test_create():
    assert factory.create("add") == Add
