import sys
from datasets import load


sys.path.append(".")
sys.path.append("Benchmarks/")
sys.path.append("..")

import spacy
import asent
import ndjson

d = asent.lexicons.get("lexicon_da_v1")
d_match = [{"label": "positive", "pattern": [{"lemma": word}]} if value > 0 else {"label": "negative", "pattern": [{"lemma": word}]}   for word, value in d.items()]

with open("prodigy/da_match_patterns.jsonl", "w") as f:
    ndjson.dump(d_match, f)

nlp = spacy.load("da_core_news_lg")


from spacy.matcher import Matcher
matcher = Matcher(nlp.vocab, validate=True)
matcher.add_pattern("")

def load_angrytweets():
    from datasets import load_dataset

    dataset = load_dataset("DDSC/angry-tweets")
    ds = dataset["train"]
    return ds["text"], ds["label"]


gen = (text for text in load_angrytweets()[0])
text = next(gen)
doc = nlp(text)
matches = matcher(doc)
for match_id, start, end in matches:
    string_id = nlp.vocab.strings[match_id]  # Get string representation
    span = doc[start:end]  # The matched span
    print(match_id, string_id, start, end, span.text)