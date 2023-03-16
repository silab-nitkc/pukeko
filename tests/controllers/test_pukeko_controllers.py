from pukeko.controllers import PukekoController
from pukeko.presentors import DictMemory


def test_generate_with_length():
    presentor = DictMemory()
    controller = PukekoController(presentor)
    controller.generate_inst_seq(3, "add")
    assert len(presentor.get_last_output()) == 3


def test_generate_inst_seq():
    presentor = DictMemory()
    controller = PukekoController(presentor)
    controller.generate_inst_seq(1, "sub")
    assert presentor.get_last_output() == [
        {"name": "sub", "operands": [0, 1], "init_num": 2}
    ]
