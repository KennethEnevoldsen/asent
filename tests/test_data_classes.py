import pytest
import spacy
from asent.data_classes import (
    DocPolarityOutput,
    SpanPolarityOutput,
    TokenPolarityOutput,
)
from spacy.tokens import Doc


@pytest.fixture()
def sample_doc() -> Doc:
    nlp = spacy.blank("en")
    doc = nlp("sample documents")
    return doc


def test_TokenPolarityOutput(sample_doc: Doc):
    t1 = TokenPolarityOutput(polarity=1, token=sample_doc[0], span=sample_doc[:])
    t2 = TokenPolarityOutput(polarity=2, token=sample_doc[0], span=sample_doc[:])

    print(t1)
    assert t1 != t2
    assert t1 < t2
    assert t2 > t1


def test_SpanPolarityOutput(sample_doc: Doc):
    tok = TokenPolarityOutput(polarity=1, token=sample_doc[0], span=sample_doc[:])
    t1 = SpanPolarityOutput(
        negative=0,
        neutral=0,
        positive=0,
        compound=1,
        span=sample_doc[:],
        polarities=[tok],
    )
    t2 = SpanPolarityOutput(
        negative=0,
        neutral=0,
        positive=0,
        compound=2,
        span=sample_doc[:],
        polarities=[tok],
    )

    print(t1)
    assert t1 != t2
    assert t1 < t2
    assert t2 > t1


def test_DocPolarityOutput(sample_doc: Doc):
    tok = TokenPolarityOutput(polarity=1, token=sample_doc[0], span=sample_doc[:])
    span = SpanPolarityOutput(
        negative=0,
        neutral=0,
        positive=0,
        compound=1,
        span=sample_doc[:],
        polarities=[tok],
    )

    t1 = DocPolarityOutput(
        negative=0,
        neutral=0,
        positive=0,
        compound=1,
        polarities=[span],
        doc=sample_doc,
    )
    t2 = DocPolarityOutput(
        negative=0,
        neutral=0,
        positive=0,
        compound=2,
        polarities=[span],
        doc=sample_doc,
    )

    print(t1)
    assert t1 != t2
    assert t1 < t2
    assert t2 > t1
