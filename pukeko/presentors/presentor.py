from abc import ABCMeta, abstractmethod


class Presentor(metaclass=ABCMeta):
    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def push(self) -> None:
        pass

    @abstractmethod
    def end(self) -> None:
        pass

    @abstractmethod
    def get_last_output(self) -> None:
        pass
