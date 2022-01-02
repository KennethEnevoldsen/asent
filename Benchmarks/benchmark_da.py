"""
A benchmark script for the Danish pipelines
"""

import sys
from typing import Callable, Dict


sys.path.append(".")
sys.path.append("benchmark/")
sys.path.append("..")


from benchmark import validate_datasets, show_n_incorrect

import asent
import spacy


da_components = [
    c for c in asent.components.get_all().keys() if c.split("_")[1] == "da"
]


def load_europarl1():
    from danlp.datasets import EuroparlSentiment1

    eurosent = EuroparlSentiment1()

    df = eurosent.load_with_pandas()
    return df["text"], df["valence"]


def load_europarl2():
    from datasets import load_dataset

    dataset = load_dataset("DDSC/europarl")
    ds = dataset["train"]
    return ds["text"], ds["label"]


def load_lccsent():
    from datasets import load_dataset

    dataset = load_dataset("DDSC/lcc")
    ds = dataset["train"]
    return ds["text"], ds["label"]


def load_angrytweets():
    from datasets import load_dataset

    dataset = load_dataset("DDSC/angry-tweets")
    ds = dataset["train"]
    return ds["text"], ds["label"]


def load_twittersent():
    from datasets import load_dataset

    dataset = load_dataset("DDSC/twitter-sent")
    ds = dataset["train"]
    return ds["text"], ds["label"]


danish_datasets = {
    "europarl1": load_europarl1,
    "europarl2": load_europarl2,
    "lccsent": load_lccsent,
    "angry-tweets": load_angrytweets,
    "twitter-sent": load_twittersent,
}

c = da_components[0]
nlp = spacy.load("da_core_news_lg")
nlp.add_pipe(c, config={"force": True})

validate_datasets(nlp, danish_datasets)

from asent.getters import make_valance_getter, make_is_negated_getter, make_is_negation_getter, make_intensifier_getter
asent.lexicons.get("lexicon_da_v1")

da_getters = {} 

def make_valence_getters():
    getters = {}
    getters["valence_standard"] = make_valance_getter(lexicon=asent.lexicons.get("lexicon_da_v1"), lemmatize=True, lowercase=True, cap_differential=True)
    getters["valence_no_cap"] = make_valance_getter(lexicon=asent.lexicons.get("lexicon_da_v1"), lemmatize=True, lowercase=True, cap_differential=False)
    getters["valence_no_lemma"] = make_valance_getter(lexicon=asent.lexicons.get("lexicon_da_v1"), lemmatize=False, lowercase=True, cap_differential=False)

    getters["standard_valence"] = make_valance_getter(lexicon=asent.lexicons.get("lexicon_da_afinn"), lemmatize=True, lowercase=True, cap_differential=True)
    getters["valence_no_cap"] = make_valance_getter(lexicon=asent.lexicons.get("lexicon_da_afinn"), lemmatize=True, lowercase=True, cap_differential=False)
    getters["valence_no_lemma"] = make_valance_getter(lexicon=asent.lexicons.get("lexicon_da_afinn"), lemmatize=False, lowercase=True, cap_differential=False)

    # sentida1

def make_is_negated_getters():
    getters = {}
    neg = make_is_negation_getter(negations=asent.lexicons.get("negations_da_v1"), lemmatize=True, lowercase=True)
    getters["is_negated_standard"] = make_is_negated_getter(is_negation_getter=neg)
    neg = make_is_negation_getter(negations={}, lemmatize=True, lowercase=True)
    getters["is_negated_no_negations"] = make_is_negated_getter(is_negation_getter=neg)
    
    neg = ...
    getters["is_negated_with_morph_neg"] = make_is_negated_getter(is_negation_getter=neg)

    neg = ...
    getters["is_negated_with_dep_neg"] = make_is_negated_getter(is_negation_getter=neg)

    neg = ...
    getters["is_negated_with_dep_and_morph"] = make_is_negated_getter(is_negation_getter=neg)



def make_is_intensifiers_getters():
    getters = {}
    getters["intensifier_standard"] = make_intensifier_getter(intensifiers=asent.lexicons("intensifiers_da_v1"), lemmatize=True)
    getters["intensifier_no_cap_diff"] = make_intensifier_getter(intensifiers=asent.lexicons("intensifiers_da_v1"), lemmatize=True, cap_differential=False)
    getters["intensifier_no_intensifiers"] = make_intensifier_getter(intensifiers={})
    # getters["intensifier_with_dep_lemma"] = ...
    # getters["intensifier_with_dep_no_lemma"] = ...

def make_span_polarity_getters():
    # with but
    # without but

    # with without exclamation
    # with without questionmarks
    


def grid_search(nlp, getters = Dict[str, Callable]):
    pass

# texts, pred = danish_datasets["twitter-sent"]()

# show_n_incorrect(nlp, texts, pred)
