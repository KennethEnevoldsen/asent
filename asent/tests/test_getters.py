import pytest

import spacy
from spacy.tokens import Token, Span

from asent.getters import (
    make_valance_getter,
    make_is_negated_getter,
    make_token_polarity_getter,
    make_span_polarity_getter,
)

nlp = spacy.load("da_core_news_lg")


EXAMPLES = [
    "jeg er glad",
    "jeg er GLAD",
    "jeg er sur",
    "jeg er ikke sur",
    "jeg er ikke længere sur",
    "jeg er ikke længere særligt sur",
    "jeg er meget glad",
    "jeg er ikke glad",
    "filmen var okay god men er generelt skuffet",
    "filmen var okay god, er generelt skuffet",
]


def test_valence_getter():
    Token.set_extension("valence", getter=make_valance_getter())

    docs = [nlp(e) for e in EXAMPLES[:3]]

    assert docs[0][-1]._.valence > 0
    assert docs[1][-1]._.valence > 0
    assert docs[2][-1]._.valence < 0

    assert docs[0][-1]._.valence < docs[1][-1]._.valence
    assert docs[2][-1]._.valence < docs[0][-1]._.valence


def test_is_negation():
    Token.set_extension("is_negated", getter=make_is_negated_getter())

    docs = [nlp(e) for e in EXAMPLES[0:6]]

    for d in docs[:3]:
        assert not d[-1]._.is_negated
    for d in docs[3:6]:
        assert d[-1]._.is_negated


def test_token_polarity():
    Token.set_extension("polarity", getter=make_token_polarity_getter())

    sents = list(
        filter(
            lambda x: x,
            [
                sent
                for e in [EXAMPLES[0], EXAMPLES[6], EXAMPLES[7]]
                for sent in nlp(e).sents
            ],
        )
    )

    assert sents[0][-1]._.polarity < sents[1][-1]._.polarity
    assert sents[0][-1]._.polarity > sents[2][-1]._.polarity


def test_span_polarity():
    Span.set_extension(
        "polarity",
        getter=make_span_polarity_getter(),
    )

    sents = list(filter(lambda x: x, [sent for e in EXAMPLES for sent in nlp(e).sents]))

    assert sents[0]._.polarity.compound > 0
    assert sents[1]._.polarity.compound > sents[0]._.polarity.compound
    assert sents[2]._.polarity.compound < 0
    assert sents[8]._.polarity.compound < sents[9]._.polarity.compound
