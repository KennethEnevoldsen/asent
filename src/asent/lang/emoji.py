import json
import os

from ..utils import lexicons


def read_emoji():  # noqa
    path = os.path.join(  # noqa
        os.path.dirname(os.path.abspath(__file__)),  # noqa
        "..",
        "lexicons",
        "emoji_v1.json",
    )
    with open(path) as f:  # noqa
        emoji_lexicon = json.load(f)
    return emoji_lexicon


LEXICON = read_emoji()

lexicons.register("emoji_v1", func=LEXICON)
