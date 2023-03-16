from pukeko.operators import factory
import pytest


@pytest.mark.skip(reason="Notは廃止された")
def test_id():
    assert factory.create("not").get_id() == 5
    assert factory.create("not").get_name() == "not"


@pytest.mark.skip(reason="Notは廃止された")
def test_calc():
    assert factory.create("not").calc(1) == -2
