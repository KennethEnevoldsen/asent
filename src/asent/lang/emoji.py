import json
import os

from ..utils import lexicons


def read_emoji():
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "lexicons",
        "emoji_v1.json",
    )
    with open(path) as f:
        emoji_lexicon = json.load(f)
    return emoji_lexicon


LEXICON = read_emoji()

lexicons.register("emoji_v1", func=LEXICON)
