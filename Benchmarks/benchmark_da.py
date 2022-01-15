"""
A benchmark script for the Danish pipelines
"""

import sys


sys.path.append(".")
sys.path.append("Benchmarks/")
sys.path.append("..")


from benchmark import validate_datasets, show_n_incorrect, to_categorical

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
    "europarl1": load_europarl1(),
    "europarl2": load_europarl2(),
    "lccsent": load_lccsent(),
    "angry-tweets": load_angrytweets(),
    "twitter-sent": load_twittersent(),
}

c = da_components[0]
nlp = spacy.load("da_core_news_lg")
nlp.add_pipe(c, config={"force": True})
from asent.getters import make_valance_getter

v_getter = make_valance_getter(
    lexicon=asent.lexicons.get("lexicon_da_afinn_v1"),
    lemmatize=False,
    lowercase=True,
    cap_differential=False,
)
from spacy.tokens import Token

Token.set_extension("valence", getter=v_getter, force=True)

res = validate_datasets(nlp, danish_datasets)

[(t,r) for t, r in zip(danish_datasets["europarl1"][0], danish_datasets["europarl1"][1]) if "Hr. formand" in t]


import numpy as np
res = show_n_incorrect(
    nlp,
    texts=danish_datasets["europarl1"][0],
    y_true=to_categorical(np.array(danish_datasets["europarl1"][0])),
    y_pred=to_categorical(
        np.array([d._.polarity.compound for d in nlp.pipe(danish_datasets["europarl1"][0])])
    ),n=10
)

print(res["angry-tweets"]["Classification Report"])
print(res["angry-tweets"]["Confusion Matrix"])


def make_valence_getters():
    from asent.getters import make_valance_getter

    getters = {}
    getters["valence_standard"] = make_valance_getter(
        lexicon=asent.lexicons.get("lexicon_da_v1"),
        lemmatize=True,
        lowercase=True,
        cap_differential=True,
    )
    getters["valence_no_cap"] = make_valance_getter(
        lexicon=asent.lexicons.get("lexicon_da_v1"),
        lemmatize=True,
        lowercase=True,
        cap_differential=False,
    )
    getters["valence_no_lemma"] = make_valance_getter(
        lexicon=asent.lexicons.get("lexicon_da_v1"),
        lemmatize=False,
        lowercase=True,
        cap_differential=False,
    )

    getters["valence_no_lemma"] = make_valance_getter(
        lexicon=asent.lexicons.get("lexicon_da_v1"),
        lemmatize=False,
        lowercase=True,
        cap_differential=False,
    )

    getters["valence_afinn"] = make_valance_getter(
        lexicon=asent.lexicons.get("lexicon_da_afinn_v1"),
        lemmatize=True,
        lowercase=True,
        cap_differential=True,
    )
    getters["valence_no_cap_afinn"] = make_valance_getter(
        lexicon=asent.lexicons.get("lexicon_da_afinn_v1"),
        lemmatize=True,
        lowercase=True,
        cap_differential=False,
    )
    getters["valence_no_lemma_afinn"] = make_valance_getter(
        lexicon=asent.lexicons.get("lexicon_da_afinn_v1"),
        lemmatize=False,
        lowercase=True,
        cap_differential=False,
    )
    # sentida1
    return getters


def make_is_negated_getters():
    from asent.getters import make_is_negated_getter, make_is_negation_getter
    from new_funcs import is_negation, is_negated
    from functools import partial

    getters = {}
    neg = make_is_negation_getter(
        negations=asent.lexicons.get("negations_da_v1"), lemmatize=True, lowercase=True
    )
    getters["is_negated_standard"] = make_is_negated_getter(is_negation_getter=neg)
    neg = make_is_negation_getter(negations={}, lemmatize=True, lowercase=True)
    getters["is_negated_no_negations"] = make_is_negated_getter(is_negation_getter=neg)

    getters["is_negated_with_morph_neg"] = make_is_negated_getter(
        is_negation_getter=is_negation
    )

    neg = make_is_negation_getter(
        negations=asent.lexicons.get("negations_da_v1"), lemmatize=True, lowercase=True
    )
    getters["is_negated_with_dep_neg"] = partial(is_negated, is_negation_getter=neg)
    getters["is_negated_with_dep_and_morph"] = partial(
        is_negated, is_negation_getter=is_negation
    )
    return getters


def make_is_intensifiers_getters():
    from asent.getters import make_intensifier_getter

    getters = {}
    getters["intensifier_standard"] = make_intensifier_getter(
        intensifiers=asent.lexicons("intensifiers_da_v1"), lemmatize=True
    )
    getters["intensifier_no_cap_diff"] = make_intensifier_getter(
        intensifiers=asent.lexicons("intensifiers_da_v1"),
        lemmatize=True,
        # cap_differential=False,
    )
    getters["intensifier_no_intensifiers"] = make_intensifier_getter(intensifiers={})
    # intensifiers filtered to adv and adj
    # getters["intensifier_filtered_lemma"] = ...
    # getters["intensifier_filtered_no_lemma"] = ...
    return getters


def make_token_polarity_getters():
    from asent.getters import make_token_polarity_getter

    getters = {}
    getters["token_polarity_standard"] = make_token_polarity_getter()
    # with dep intensifiers lookback
    return getters


def make_span_polarity_getters():
    from asent.getters import make_span_polarity_getter, make_is_contrastive_conj_getter

    getters = {}
    cconj_getter = make_is_contrastive_conj_getter(
        asent.lexicons.get("contrastive_conj_da_v1")
    )
    getters["span_polarity_standard"] = make_span_polarity_getter(
        polarity_getter=None, contrastive_conj_getter=cconj_getter
    )

    cconj_getter = make_is_contrastive_conj_getter(
        asent.lexicons.get("contrastive_conj_da_v1"), lemmatize=False
    )
    getters["span_polarity_cconj_lemma"] = make_span_polarity_getter(
        polarity_getter=None, contrastive_conj_getter=cconj_getter
    )

    cconj_getter = make_is_contrastive_conj_getter({})
    getters["span_polarity_no_cconj"] = make_span_polarity_getter(
        polarity_getter=None, contrastive_conj_getter=cconj_getter
    )

    # with dep/pos but
    # with without exclamation
    # with without questionmarks
    return getters


def make_doc_polarity_getters():
    from asent.getters import make_doc_polarity_getter

    getters = {}
    getters["doc_polarity_standard"] = make_doc_polarity_getter(
        span_polarity_getter=None
    )

    from afinn import Afinn

    afinn = Afinn(language="da")

    def afinn_getter(doc):
        return afinn.score(doc.text)

    getters["doc_polarity_afinn"] = afinn_getter

    return getters


def make_da_getters_grid():
    getters = {
        "Token": {
            "valence": make_valence_getters(),
            "is_negated": make_is_negated_getters(),
            "is_intensifier": make_is_intensifiers_getters(),
            "polarity": make_token_polarity_getters(),
        },
        "Span": {"polarity": make_span_polarity_getters()},
        "Doc": {"polarity": make_doc_polarity_getters()},
    }
    return getters


def grid_search(nlp, grid=make_da_getters_grid(), datasets=danish_datasets):
    from spacy.tokens import Token, Span, Doc

    queue = [
        (obj, ext, getter_name, getter)
        for obj, obj_dict in grid.items()
        for ext, ext_dict in obj_dict.items()
        for getter_name, getter in ext_dict.items()
    ]

    def assign_ext(obj, ext, getter):
        if obj.lower() == "token":
            Token.set_extension(ext, getter=getter, force=True)
        if obj.lower() == "span":
            Span.set_extension(ext, getter=getter, force=True)
        if obj.lower() == "doc":
            Doc.set_extension(ext, getter=getter, force=True)

    results = []
    while queue:
        obj, ext, getter_name, getter = queue.pop()
        print(getter_name)

        results_ = {}
        results_["assigned_getters"] = []

        # set extensions
        assign_ext(obj, ext, getter)
        results_["assigned_getters"].append((obj, ext, getter_name))

        results_["performance"] = validate_datasets(nlp, datasets, verbose=False)
        results.append(results_)

    return results


import pandas as pd
import numpy as np

grid = make_da_getters_grid()
[grid.pop(k) for k in list(grid.keys()) if k != "Token"]
[grid["Token"].pop(k) for k in list(grid["Token"].keys()) if k != "valence"]


res = grid_search(nlp, grid=grid)


from copy import deepcopy

sav = deepcopy(res)


# import pickle
# with open("tmp.pkl", "wb") as f:
#     pickle.dump(sav, f)

for d in res:
    ds = d.pop("performance")
    for ds_name, ds_dict in ds.items():
        for k, val in ds_dict.items():
            d[f"{ds_name}_{k}"] = val


df = pd.DataFrame(res)
df
