from . import Presentor


class DictMemory(Presentor):
    def __init__(self) -> None:
        self.last_output = []

    def run(self, target: list[dict]) -> None:
        self.last_output = target

    def start(self) -> None:
        self.last_output = []

    def push(self, target: dict) -> None:
        self.last_output = target

    def end(self) -> None:
        pass

    def get_last_output(self) -> list[dict]:
        return self.last_output
