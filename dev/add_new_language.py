"""Convert into sentiment lexicon from:

https://www.kaggle.com/datasets/rtatman/sentiment-lexicons-
for-81-languages/discussion/39827?resource=download into txt files for
each language with each positive word rated +1 and negative words rated
-1.
"""
from collections import defaultdict
from pathlib import Path

path = Path("/Users/au561649/Downloads/archive")

rated_words = defaultdict(list)
for w_path in set(path.glob("sentiment-lexicons/*.txt")):
    lang_id = w_path.stem.split("_")[-1]
    is_positive = w_path.stem.split("_")[0] == "positive"
    rating = 1 if is_positive else -1
    with open(path / w_path) as f:
        words = list(filter(lambda x: x, f.read().split("\n")))
    words = [(w, rating) for w in words]
    rated_words[lang_id] += words

lexicon_path = Path("/Users/au561649/Desktop/Github/asent/asent/lexicons")
for lang_id in rated_words:
    with open(lexicon_path / f"{lang_id}_lexicon_chen_skiena_2014_v1.txt", "w") as f:
        txt = "\n".join(["\t".join([str(i) for i in w]) for w in rated_words[lang_id]])
        f.write(txt)
