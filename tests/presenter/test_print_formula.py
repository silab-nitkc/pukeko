from pukeko.presentors import PrintFormula


def test_format_single_inst():
    target = [{"name": "add", "operands": [0, 1], "init_num": 2}]
    res = PrintFormula()._format_as_formula(target)
    assert res == r"%0 + %1"


def test_format_inst_seq():
    target = [
        {
            "name": "add",
            "operands": [0, 1],
            "init_num": 2,
        },
        {
            "name": "and",
            "operands": [1, 2],
        },
        {
            "name": "add",
            "operands": [1, 3],
        },
    ]
    res = PrintFormula()._format_as_formula(target)
    assert res == r"%1 + (%1 & (%0 + %1))"
