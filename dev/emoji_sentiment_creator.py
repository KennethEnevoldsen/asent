import codecs
import json
import os
from inspect import getsourcefile

import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def read_emoji_as_dict():
    _this_module_file_path_ = os.path.abspath(getsourcefile(lambda: 0))
    emoji_lexicon = "emoji_utf8_lexicon.txt"
    emoji_full_filepath = os.path.join(
        os.path.dirname(_this_module_file_path_),
        emoji_lexicon,
    )
    with codecs.open(emoji_full_filepath, encoding="utf-8") as f:
        emoji_dict = {}
        for line in f.read().rstrip("\n").split("\n"):
            (emoji, description) = line.strip().split("\t")[0:2]
            emoji_dict[emoji] = description
    return emoji_dict


def get_lexicon_min_max():
    os.chdir("..")
    from sentida.constants import LEXICON

    arr = np.array([float(t) for _, t in LEXICON.items()])
    return arr.min(), arr.max()


e_dict = read_emoji_as_dict()
lmin, lmax = get_lexicon_min_max()

analyzer = SentimentIntensityAnalyzer()
rated = {
    emoji: analyzer.polarity_scores(text)["compound"] for emoji, text in e_dict.items()
}


def normalize_emoji_to_min_max():
    def replace_0_na(x):
        if x == 0:
            return np.nan
        return x

    x = np.array([replace_0_na(t) for _, t in rated.items()])
    x_scaled = lmin + (x - min(x)) * (lmax - lmin) / (max(x) - min(x))
    x_scaled[np.isnan(x_scaled)] = 0
    return {e: s for e, s in zip(rated.keys(), x_scaled)}


rated_scaled = normalize_emoji_to_min_max()


os.chdir("sentida")
with open("emoji_utf8_lexicon.json", "w") as f:
    json.dump(rated_scaled, f)
