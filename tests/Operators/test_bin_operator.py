from pukeko.operators import factory


def test_format():
    target = {"name": "add", "operands": [0, 1]}

    operator = factory.create(target["name"])
    assert operator.format(target) == r"%0 + %1"
