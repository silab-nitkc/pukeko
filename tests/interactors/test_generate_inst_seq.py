from pukeko.interactors import GenerateInstSeq
from pukeko.presentors import DictMemory
from pukeko import ConfigLoader

ConfigLoader.load()
ConfigLoader.config["atLeastOnce"] = []


def test_generate_and_test():
    presentor = DictMemory()
    interactor = GenerateInstSeq(presentor)
    interactor.generate_inst_seq(3, {"name": "add", "operands": [0, 1]})
    assert len(presentor.get_last_output()) == 3


def test_valid_inst_seq():
    interactor = GenerateInstSeq()
    res = interactor.test(
        {"name": "add", "operands": [0, 1]},
        [
            {"name": "add", "operands": [0, 1]},
            {"name": "add", "operands": [0, 2]},
            {"name": "sub", "operands": [3, 0]},
        ],
    )

    assert res is True


def test_invalid_inst_seq():
    interactor = GenerateInstSeq()
    res = interactor.test(
        {"name": "add", "operands": [0, 1]},
        [{"name": "sub", "operands": [1, 0]}],
    )
    assert res is False
