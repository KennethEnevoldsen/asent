import pytest

import spacy
from spacy.tokens import Token, Span, Doc

import asent

from asent.getters import (
    make_intensifier_getter,
    make_is_contrastive_conj_getter,
    make_valance_getter,
    make_is_negated_getter,
    make_token_polarity_getter,
    make_span_polarity_getter,
    make_doc_polarity_getter,
    make_is_negation_getter,
)


@pytest.fixture()
def nlp_da():
    nlp = spacy.load("da_core_news_lg")
    return nlp


@pytest.mark.parametrize(
    "example,idx,expected,lang",
    [
        ("jeg er glad", -1, "positive", "da"),
        ("jeg er GLAD", -1, "positive", "da"),
        ("jeg er sur", -1, "negative", "da"),
    ],
)
def test_valence_getter(example, idx, expected, lang: str, nlp_da):

    if lang == "da":
        nlp = nlp_da
        lexicon = asent.lexicons.get("lexicon_da_v1")

    Token.set_extension("valence", getter=make_valance_getter(lexicon=lexicon), force=True)
    doc = nlp(example)

    if expected == "positive":
        assert doc[idx]._.valence > 0
    elif expected == "negative":
        assert doc[idx]._.valence < 0
    elif expected == "neutral":
        assert doc[idx]._.valence == 0
    else:
        raise ValueError(
            "Invalid expected value '{expected}', should be either 'positive' or 'negative'"
        )


@pytest.mark.parametrize(
    "example,cased_example,idx,lang",
    [
        ("jeg er glad", "jeg er GLAD", -1, "da"),
        ("jeg er sur", "jeg er SUR", -1, "da"),
    ],
)
def test_valence_getter_casing(example, cased_example, idx, lang, nlp_da):
    if lang == "da":
        nlp = nlp_da
        lexicon = asent.lexicons.get("lexicon_da_v1")

    Token.set_extension("valence", getter=make_valance_getter(lexicon=lexicon), force=True)

    docs = [nlp(t) for t in [example, cased_example]]
    assert abs(docs[0][idx]._.valence) < abs(docs[1][idx]._.valence)


@pytest.mark.parametrize(
    "example,idx,is_negated,lang",
    [
        ("jeg er glad", -1, False, "da"),
        ("jeg er GLAD", -1, False, "da"),
        ("jeg er sur", -1, False, "da"),
        ("jeg er ikke sur", -1, True, "da"),
        ("jeg er ikke længere sur", -1, True, "da"),
        ("jeg er ikke længere særligt sur", -1, True, "da"),
    ],
)
def test_is_negation(example, idx, is_negated, lang: str, nlp_da):

    if lang == "da":
        nlp = nlp_da
        negations = asent.lexicons.get("negations_da_v1")

    is_negation_getter = make_is_negation_getter(negations=negations)
    is_negated_getter = make_is_negated_getter(is_negation_getter=is_negation_getter)
    Token.set_extension(name="is_negated", getter=is_negated_getter, force=True)
    doc = nlp(example)
    assert doc[idx]._.is_negated is is_negated


@pytest.mark.parametrize(
    "example,idx,more_positive_example,more_positive_idx,lang",
    [
        ("jeg er glad", -1, "jeg er GLAD", -1, "da"),
        ("jeg er ikke glad", -1, "jeg er glad", -1, "da"),
    ],
)
def test_token_polarity(
    example: str,
    idx: int,
    more_positive_example: str,
    more_positive_idx: int,
    lang: str,
    nlp_da,
):
    if lang == "da":
        nlp = nlp_da
        lexicon = asent.lexicons.get("lexicon_da_v1")
        negations = asent.lexicons.get("negations_da_v1")
        intensifiers = asent.lexicons.get("intensifiers_da_v1")
        lowercase = True
        lemmatize = True

    valence_getter = make_valance_getter(
        lexicon=lexicon, lowercase=lowercase, lemmatize=lemmatize
    )
    is_negation_getter = make_is_negation_getter(negations=negations)
    intensifier_getter = make_intensifier_getter(
        intensifiers=intensifiers, lowercase=lowercase, lemmatize=lemmatize
    )

    polarity_getter = make_token_polarity_getter(
        valence_getter=valence_getter,
        is_negation_getter=is_negation_getter,
        intensifier_getter=intensifier_getter,
    )
    Token.set_extension("polarity", getter=polarity_getter, force=True)

    docs = [nlp(e) for e in [example, more_positive_example]]
    assert docs[0][idx]._.polarity < docs[1][more_positive_idx]._.polarity


@pytest.mark.parametrize(
    "example,expected,lang",
    [
        ("jeg er glad", "positive", "da"),
        ("jeg er sur", "negative", "da"),
        ("filmen var okay god men er generelt skuffet", "negative", "da"),
    ],
)
def test_span_doc_polarity(example: str, expected: str, lang: str, nlp_da):
    if lang == "da":
        nlp = nlp_da
        lexicon = asent.lexicons.get("lexicon_da_v1")
        negations = asent.lexicons.get("negations_da_v1")
        intensifiers = asent.lexicons.get("intensifiers_da_v1")
        contrast_conj = asent.lexicons.get("contrastive_conj_da_v1")
        lowercase = True
        lemmatize = True

    valence_getter = make_valance_getter(
        lexicon, lowercase=lowercase, lemmatize=lemmatize
    )
    is_negation_getter = make_is_negation_getter(negations)
    intensifier_getter = make_intensifier_getter(
        intensifiers, lowercase=lowercase, lemmatize=lemmatize
    )
    polarity_getter = make_token_polarity_getter(
        valence_getter=valence_getter,
        is_negation_getter=is_negation_getter,
        intensifier_getter=intensifier_getter,
    )
    contrastive_conj_getter = make_is_contrastive_conj_getter(contrast_conj)
    span_polarity_getter = make_span_polarity_getter(
        polarity_getter, contrastive_conj_getter=contrastive_conj_getter
    )
    doc_polarity_getter = make_doc_polarity_getter(span_polarity_getter)
    Doc.set_extension("polarity", getter=doc_polarity_getter, force=True)
    doc = nlp(example)
    sent = [s for s in doc.sents][0]  # assuming there is only one sentence
    assert doc._.polarity.compound == sent._.polarity.compound
    if expected == "positive":
        assert sent._.polarity.compound > 0
    elif expected == "negative":
        assert sent._.polarity.compound < 0
    else:
        raise ValueError(
            "Invalid expected value '{expected}', should be either 'positive' or 'negative'"
        )


@pytest.mark.parametrize(
    "example,more_positive_example,lang",
    [
        ("jeg er sur", "jeg er glad", "da"),
        ("jeg er SUR", "jeg er sur", "da"),
        (
            "filmen var okay god men er generelt skuffet",
            "filmen var okay god, er generelt skuffet",
            "da",
        ),
    ],
)
def test_span_polarity_contrast(example: str, more_positive_example: str, lang: str, nlp_da):
    if lang=="da":
        nlp = nlp_da
        nlp.add_pipe("asent_da_v1", config={"force": True})

    docs = [nlp(e) for e in [example, more_positive_example]]
    assert docs[0]._.polarity.compound < docs[1]._.polarity.compound
