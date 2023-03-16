import json
from pathlib import Path

config = {"outputOperators": [], "targetOperators": [], "atLeastOnce": []}


def load(path: Path = Path(__file__).parent / "settings.json"):
    global config
    try:
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except:
        pass
