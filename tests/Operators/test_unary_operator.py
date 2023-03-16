from pukeko.operators import factory
import pytest


@pytest.mark.skip(reason="Notは廃止された")
def test_format():
    target = {
        "name": "not",
        "operands": [1],
    }

    operator = factory.create(target["name"])
    assert operator.format(target) == r"~%1"
