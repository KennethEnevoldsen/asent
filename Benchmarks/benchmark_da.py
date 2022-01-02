"""
A benchmark script for the Danish pipelines
"""

import sys

sys.path.append(".")
import os
os.chdir("..")

from typing import Iterable, List, Tuple

import numpy as np
import asent
import spacy
from spacy.language import Language

from sklearn.metrics import f1_score, confusion_matrix, accuracy_score

da_components = [
    c for c in asent.components.get_all().keys() if c.split("_")[1] == "da"
]


def load_europarl1():
    from danlp.datasets import EuroparlSentiment1

    eurosent = EuroparlSentiment1()

    df = eurosent.load_with_pandas()
    return df["text"], df["valence"]


def load_europarl2():
    from danlp.datasets import EuroparlSentiment2

    eurosent = EuroparlSentiment2()

    df = eurosent.load_with_pandas()
    return df["text"], df["polarity"]


def load_lccsent():
    from danlp.datasets import LccSentiment

    lccsent = LccSentiment()

    df = lccsent.load_with_pandas()
    return df["text"], df["valence"]


danish_datasets = {
    "europarl1": load_europarl1,
    "europarl2": load_europarl2,
    "lccsent": load_lccsent,
}


def to_pos_neg_neutral(
    value: np.ndarray, neutral_range: Tuple[float, float] = (0, 0)
) -> np.ndarray:
    """Convert np array to 0, 1, -1 indicating neutral, postive, negative respectively."""
    v = value.copy()

    # if it is string
    if isinstance(value[0], str):
        v = np.zeros(value.shape)
        value_ = np.array([x.lower() for x in value])
        v[np.isin(value_, {"pos", "positive"})] = 1
        v[np.isin(value_, {"neg", "negative"})] = -1
        v[np.isin(value_, {"neu", "neutral"})] = 0
    else:
        v[(value >= neutral_range[0]) & (value <= neutral_range[1])] = 0
        v[value < neutral_range[0]] = -1
        v[value > neutral_range[1]] = 1
    return v


def find_optimal_neutral_range(preds, y_true, range_ = [t/100 for t in range(100)], verbose=False):
    best = ((0, 0), 0)
    for t in range_:
        y_pred = to_pos_neg_neutral(np.array(preds), neutral_range = (t, t))
        f1 = f1_score(y_true, y_pred, average="macro")
        acc = accuracy_score(y_true, y_pred)
        if verbose:
            print(f"[{t}] F1: {f1}, acc: {acc}")
        if f1 > best[1]:
            best = ((t, t), f1)
    return best 


for name, loader in danish_datasets.items():
    texts, sent = loader()

    # setup asent pipeline
    c = da_components[0]
    nlp = spacy.load("da_core_news_lg")
    nlp.add_pipe(c, config={"force": True})

    preds = [doc._.polarity.compound for doc in nlp.pipe(texts)]


    y_true = to_pos_neg_neutral(np.array(sent))
    best_range = find_optimal_neutral_range(preds, y_true, verbose=True)
    y_pred = to_pos_neg_neutral(np.array(preds), neutral_range=best_range[0])
    conf = confusion_matrix(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average="macro")
    acc = accuracy_score(y_true, y_pred)

    print(f"Dataset: {name}")
    print(f"\tAccuracy: {acc:.2f} - Macro F1: {f1:.2f} - Range: {best_range[0]}")


def show_n_incorrect(
    nlp: Language, texts: np.ndarray, y_true: np.ndarray, y_pred: np.ndarray, n=1, analysis=False
):
    import random

    w_texts = texts[y_true != y_pred]
    w_y_true = y_true[y_true != y_pred]
    w_y_pred = y_pred[y_true != y_pred]
    wrong_shuffled = [
        (t, true, pred) for t, true, pred in zip(w_texts, w_y_true, w_y_pred)
    ]
    random.shuffle(wrong_shuffled)
    for i, t in zip(range(n), wrong_shuffled):
        print(f"True: {t[1]} -  Predicted: {t[2]}")
        doc = nlp(t[0])
        asent.visualize(doc)
        if analysis is True:
            asent.visualize(doc, style="analysis")
        print(doc._.polarity)

    return w_texts


texts, sent = danish_datasets["europarl2"]()
preds = [doc._.polarity.compound for doc in nlp.pipe(texts)]

y_true = to_pos_neg_neutral(np.array(sent))
y_pred = to_pos_neg_neutral(np.array(preds))
incorrect = show_n_incorrect(nlp, texts=texts, y_true=y_true, y_pred=y_pred)
