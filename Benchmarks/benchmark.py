from typing import Tuple, Iterable, Optional, Union

import numpy as np
from sklearn.metrics import (
    f1_score,
    accuracy_score,
    r2_score,
    mean_squared_error,
    confusion_matrix,
    classification_report
)


from spacy.language import Language
import asent

from functools import partial


def to_categorical(
    value: np.ndarray, neutral_range: Tuple[float, float] = (0, 0)
) -> np.ndarray:
    """Convert np array to 0, 1, -1 indicating neutral, postive, negative respectively."""
    v = value.copy()

    # if it is string
    if isinstance(value[0], str):
        v = np.zeros(value.shape)
        value_ = np.array([x.lower() for x in value])
        v[np.isin(value_, np.array(["pos", "positive", "positiv"]))] = 1
        v[np.isin(value_, np.array(["neg", "negative", "negativ"]))] = -1
        v[np.isin(value_, np.array(["neu", "neutral"]))] = 0
    else:
        v[(value >= neutral_range[0]) & (value <= neutral_range[1])] = 0
        v[value < neutral_range[0]] = -1
        v[value > neutral_range[1]] = 1
    return v


def find_optimal_neutral_range(
    preds, y_true, range_=[t / 100 for t in range(100)], verbose=False
):
    best = ((0, 0), 0)
    for t in range_:
        y_pred = to_categorical(np.array(preds), neutral_range=(t, t))
        f1 = f1_score(y_true, y_pred, average="macro")
        acc = accuracy_score(y_true, y_pred)
        if verbose:
            print(f"[{t}] F1: {f1}, acc: {acc}")
        if f1 > best[1]:
            best = ((t, t), f1)
    return best[0]


def show_n_incorrect(
    nlp: Language,
    texts: np.ndarray,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    n=1,
    analysis=False,
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


def validate(
    texts: Iterable[str],
    true: Iterable[Union[float, str]],
    nlp: Language,
    search_for_best_range: bool = True,
    categorical: Optional[bool] = None,
):
    def get_score(doc):
        if isinstance(doc._.polarity, float):
            return doc._.polarity
        return doc._.polarity.compound

    preds = [get_score(doc) for doc in nlp.pipe(texts)]
    y_true = np.array(list(true))

    if isinstance(y_true[0], str) and categorical is None:
        categorical = True

    if categorical is True or categorical is None:
        c_y_true = to_categorical(np.array(y_true))
        if search_for_best_range is True:
            n_range = find_optimal_neutral_range(preds, c_y_true)
        else:
            n_range = (0, 0)
        c_preds = to_categorical(np.array(preds), neutral_range=n_range)

    metrics = {
        "Macro F1": (partial(f1_score, average="macro"), "categorical"),
        "Accuracy": (accuracy_score, "categorical"),
        "Confusion Matrix": (confusion_matrix, "categorical"),
        "Classification Report": (classification_report, "categorical"),
        "RMSE": (mean_squared_error, "Non-categorical"),
        "R2": (r2_score, "Non-categorical"),
    }

    output = {}
    if categorical is None or categorical is True:
        output["used neutral range"] = n_range
    for name, m in metrics.items():
        metric, cat = m
        if cat == "categorical" and (categorical is None or categorical is True):
            output[name] = metric(c_y_true, c_preds)
        if cat != "categorical" and (categorical is None or categorical is False):
            output[name] = metric(y_true, np.array(preds))
    return output


def validate_datasets(nlp, datasets, verbose: bool = True):
    output = {}
    for d_name, dataset in datasets.items():
        texts, true = dataset

        out = validate(texts, true, nlp)
        output[d_name] = out

        if verbose:
            print(d_name)
            print("\t", end="")

            [
                print(f"{name}: {score:.2f} - ", end="")
                for name, score in out.items()
                if isinstance(score, float)
            ]
            print(f"\tUsed neutral-range: {out['used neutral range']}")
    return output
