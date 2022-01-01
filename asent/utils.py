from typing import Callable, Dict, List
import catalogue

lexicons = catalogue.create("asent", "lexicon", entry_points=True)
components = catalogue.create("asent", "components", entry_points=True)


def register_lexicon(name: str, lexicon: Dict[str, float]) -> None:
    """Registers a lexicon in asent.lexicons

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
    """Registers a component in asent.components

    Args:
        name (str): The name of the lexicon
        func (Callable): A Callable component
    """
    components.register(name, func=func)
