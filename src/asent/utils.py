from pathlib import Path
from typing import Callable, Union

import catalogue

LEXICON_PATH = Path(__file__).parent / ".." / "asent" / "lexicons"

lexicons = catalogue.create("asent", "lexicon", entry_points=True)
components = catalogue.create("asent", "components", entry_points=True)


def register_lexicon(name: str, lexicon: dict[str, float]) -> None:
    """Registers a lexicon in asent.lexicons.

    Args:
        name (str): The name of the lexicon
        lexicon (Dict[str, float]): The lexicon supplies as a dictionary.

    Example:
        >>> asent.register("my_lexicon_v1", {"happy": 4, "sad": -2})
        >>> asent.lexicons.get("my_lexicon_v1")
        {"happy": 4, "sad": -2}
    """
    lexicons.register(name, func=lexicon)


def register_component(name: str, func: Callable) -> None:
    """Registers a component in asent.components.

    Args:
        name (str): The name of the lexicon
        func (Callable): A Callable component
    """
    components.register(name, func=func)


def read_lexicon(path: Union[str, Path]) -> dict[str, float]:
    with open(path, encoding="utf-8") as f:  # noqa
        lexicon = {}
        for line in f.read().rstrip("\n").split("\n"):
            if not line:
                continue
            (word, measure) = line.strip().split("\t")[0:2]
            lexicon[word] = float(measure)
    return lexicon
