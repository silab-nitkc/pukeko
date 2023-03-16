from base64 import encode
import json
from . import Presentor


class PrintJson(Presentor):
    def __init__(self) -> None:
        self.last_output = ""

    def run(self, target: list[dict]) -> None:
        self.last_output = json.dumps(target, indent=2)
        print(self.last_output)

    def start(self) -> None:
        self.last_output = ""
        print("[")

    def push(self, target: dict) -> None:
        if self.last_output:
            print(",")
        self.last_output = json.dumps(target, indent=2)
        self.last_output = "  " + self.last_output
        self.last_output = self.last_output.replace("\n", "\n  ")
        print(self.last_output, end="", flush=True)

    def end(self) -> None:
        print("\n]")

    def get_last_output(self) -> str:
        return self.last_output
