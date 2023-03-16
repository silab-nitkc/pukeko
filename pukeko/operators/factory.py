from . import Add, Sub, Or, And, Xor

_operators = {
    "add": Add,
    "sub": Sub,
    "or": Or,
    "and": And,
    "xor": Xor,
}


def create(name):
    return _operators[name]


def createById(id):
    return next(filter(lambda op: op.get_id() == id, _operators.values()))


def all():
    return [_operators[key] for key in _operators]
