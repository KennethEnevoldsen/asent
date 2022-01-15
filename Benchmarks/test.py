import sys


sys.path.append(".")
sys.path.append("Benchmarks/")
sys.path.append("..")

import spacy
import asent

nlp = spacy.load("da_core_news_lg")
nlp.add_pipe("asent_da_v1", config={"force": True})


from spacy.matcher import Matcher
matcher = Matcher(nlp.vocab, validate=True)
pattern = [{"LOWER": "er"}, {"_": {"valence": {">": 0}}}]
matcher.add("pos_words", [pattern])
pattern = [{"LOWER": "er"}, {"_": {"valence": {"<": 0}}}]
matcher.add("pos_words", [pattern])

doc = nlp("Flot sejr til både Mie Andersen og Lars Albræt")
doc[-1]._.polarity
matches = matcher(doc)

from spacy.matcher import DependencyMatcher

matcher = DependencyMatcher(nlp.vocab)

pattern = [
    {
        "RIGHT_ID": "anchor_valence",
        "RIGHT_ATTRS": {"_": {"valence": {"<": 0}}}
    },
    {
        "LEFT_ID": "anchor_valence",
        "REL_OP": ">",
        "RIGHT_ID": "subject",
        "RIGHT_ATTRS": {"DEP": "nsubj"},
    },
]

matcher.add("FOUNDED", [pattern])
matches = matcher(doc)

match_id, token_ids = matches[0]
for i in range(len(token_ids)):
    print(pattern[i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)
from spacy import displacy
displacy.render(doc)

def load_angrytweets():
    from datasets import load_dataset

    dataset = load_dataset("DDSC/angry-tweets")
    ds = dataset["train"]
    return ds["text"], ds["label"]

docs = [d for d in nlp.pipe(load_angrytweets()[0]) if len([e for e in d.ents if e.label_ in "PER"]) > 0]
docs[1]
displacy.render(doc)

from prodigy.components.db import connect
db = connect()                               # uses settings from prodigy.json
dataset = db.get_dataset("angrytweets_annotated")     # retrieve a dataset

dataset[0]