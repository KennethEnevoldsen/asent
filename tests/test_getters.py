import asent
import pytest
import spacy
from asent.getters import (
    make_doc_polarity_getter,
    make_intensifier_getter,
    make_is_contrastive_conj_getter,
    make_is_negated_getter,
    make_is_negation_getter,
    make_span_polarity_getter,
    make_token_polarity_getter,
    make_valance_getter,
)
from spacy.tokens import Doc, Token


@pytest.fixture()
def nlp_dict() -> dict:
    nlp_en = spacy.blank("en")
    nlp_en.add_pipe("sentencizer")
    nlp_da = spacy.load("da_core_news_sm")
    nlp_sv = spacy.blank("sv")
    nlp_sv.add_pipe("sentencizer")
    nlp_nb = spacy.blank("nb")
    nlp_nb.add_pipe("sentencizer")
    nlp_de = spacy.blank("de")
    nlp_de.add_pipe("sentencizer")

    return {"da": nlp_da, "en": nlp_en, "no": nlp_nb, "sv": nlp_sv, "de": nlp_de}


@pytest.mark.parametrize(
    ("example", "idx", "expected", "lang"),
    [
        ("jeg er glad", -1, "positive", "da"),
        ("jeg er GLAD", -1, "positive", "da"),
        ("jeg er sur", -1, "negative", "da"),
    ],
)
def test_valence_getter(
    example: str,
    idx: int,
    expected: str,
    lang: str,
    nlp_dict: dict,
):
    nlp = nlp_dict[lang]
    lexicon = asent.lexicons.get("lexicon_" + lang + "_v1")

    Token.set_extension(
        "valence",
        getter=make_valance_getter(lexicon=lexicon),
        force=True,
    )
    doc = nlp(example)

    if expected == "positive":
        assert doc[idx]._.valence > 0
    elif expected == "negative":
        assert doc[idx]._.valence < 0
    elif expected == "neutral":
        assert doc[idx]._.valence == 0
    else:
        raise ValueError(
            "Invalid expected value '{expected}', should be either 'positive' or "
            + "'negative'",
        )


@pytest.mark.parametrize(
    ("example", "cased_example", "idx", "lang"),
    [
        ("jeg er glad", "jeg er GLAD", -1, "da"),
        ("jeg er sur", "jeg er SUR", -1, "da"),
    ],
)
def test_valence_getter_casing(
    example: str,
    cased_example: str,
    idx: int,
    lang: str,
    nlp_dict: dict,
):
    nlp = nlp_dict[lang]
    lexicon = asent.lexicons.get("lexicon_" + lang + "_v1")

    Token.set_extension(
        "valence",
        getter=make_valance_getter(lexicon=lexicon),
        force=True,
    )

    docs = [nlp(t) for t in [example, cased_example]]
    assert abs(docs[0][idx]._.valence) < abs(docs[1][idx]._.valence)


@pytest.mark.parametrize(
    ("example", "idx", "is_negated", "lang"),
    [
        ("jeg er glad", -1, False, "da"),
        ("jeg er GLAD", -1, False, "da"),
        ("jeg er sur", -1, False, "da"),
        ("jeg er ikke sur", -1, True, "da"),
        ("jeg er ikke længere sur", -1, True, "da"),
        ("jeg er ikke længere særligt sur", -1, True, "da"),
    ],
)
def test_is_negation(
    example: str,
    idx: int,
    is_negated: bool,
    lang: str,
    nlp_dict: dict,
):
    nlp = nlp_dict[lang]
    negations = asent.lexicons.get("negations_" + lang + "_v1")

    is_negation_getter = make_is_negation_getter(negations=negations)
    is_negated_getter = make_is_negated_getter(is_negation_getter=is_negation_getter)
    Token.set_extension(name="is_negated", getter=is_negated_getter, force=True)
    doc = nlp(example)
    assert bool(doc[idx]._.is_negated) is is_negated


@pytest.mark.parametrize(
    ("example", "idx", "more_positive_example", "more_positive_idx", "lang"),
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
    nlp_dict: dict,
):
    nlp = nlp_dict[lang]
    lexicon = asent.lexicons.get("lexicon_" + lang + "_v1")
    negations = asent.lexicons.get("negations_" + lang + "_v1")
    intensifiers = asent.lexicons.get("intensifiers_" + lang + "_v1")

    lowercase = True
    lemmatize = False

    valence_getter = make_valance_getter(
        lexicon=lexicon,
        lowercase=lowercase,
        lemmatize=lemmatize,
    )
    is_negation_getter = make_is_negation_getter(negations=negations)
    is_negated_getter = make_is_negated_getter(is_negation_getter=is_negation_getter)
    intensifier_getter = make_intensifier_getter(
        intensifiers=intensifiers,
        lowercase=lowercase,
        lemmatize=lemmatize,
    )

    polarity_getter = make_token_polarity_getter(
        valence_getter=valence_getter,
        is_negated_getter=is_negated_getter,
        intensifier_getter=intensifier_getter,
    )
    Token.set_extension("polarity", getter=polarity_getter, force=True)

    docs = [nlp(e) for e in [example, more_positive_example]]
    assert docs[0][idx]._.polarity < docs[1][more_positive_idx]._.polarity


@pytest.mark.parametrize(
    ("example", "expected", "lang"),
    [
        ("jeg er glad", "positive", "da"),
        ("jeg er sur", "negative", "da"),
        ("jeg er sur?", "negative", "da"),
        ("jeg er sur???", "negative", "da"),
        ("jeg er sur!", "negative", "da"),
        ("jeg er sur!!!!!!", "negative", "da"),
        ("xyz", "neutral", "da"),
        ("filmen var okay god men er generelt skuffet", "negative", "da"),
        ("ich bin ser gut!", "positive", "de"),
    ],
)
def test_span_doc_polarity(example: str, expected: str, lang: str, nlp_dict: dict):
    nlp = nlp_dict[lang]
    lexicon = asent.lexicons.get("lexicon_" + lang + "_v1")

    if lang in {"da", "sv"}:
        negations = asent.lexicons.get("negations_" + lang + "_v1")
        intensifiers = asent.lexicons.get("intensifiers_" + lang + "_v1")
    else:
        negations = set()
        intensifiers = {}
    if lang in {"da"}:
        cconj = asent.lexicons.get("contrastive_conj_" + lang + "_v1")
    else:
        cconj = set()

    lowercase = True
    lemmatize = False

    valence_getter = make_valance_getter(
        lexicon,
        lowercase=lowercase,
        lemmatize=lemmatize,
    )
    is_negation_getter = make_is_negation_getter(negations)
    is_negated_getter = make_is_negated_getter(is_negation_getter=is_negation_getter)
    intensifier_getter = make_intensifier_getter(
        intensifiers,
        lowercase=lowercase,
        lemmatize=lemmatize,
    )
    polarity_getter = make_token_polarity_getter(
        valence_getter=valence_getter,
        is_negated_getter=is_negated_getter,
        intensifier_getter=intensifier_getter,
    )
    contrastive_conj_getter = make_is_contrastive_conj_getter(cconj)
    span_polarity_getter = make_span_polarity_getter(
        polarity_getter,
        contrastive_conj_getter=contrastive_conj_getter,
    )
    doc_polarity_getter = make_doc_polarity_getter(span_polarity_getter)
    Doc.set_extension("polarity", getter=doc_polarity_getter, force=True)
    doc = nlp(example)
    sent = list(doc.sents)[0]  # assuming there is only one sentence
    assert doc._.polarity.compound == sent._.polarity.compound
    if expected == "positive":
        assert sent._.polarity.compound > 0
    elif expected == "negative":
        assert sent._.polarity.compound < 0
    elif expected == "neutral":
        assert sent._.polarity.compound == 0
    else:
        raise ValueError(
            "Invalid expected value '{expected}', should be either 'neutral', "
            + "'positive' or 'negative'",
        )


@pytest.mark.parametrize(
    ("example", "more_positive_example", "lang"),
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
def test_span_polarity_contrast(
    example: str,
    more_positive_example: str,
    lang: str,
    nlp_dict: dict,
):
    nlp = nlp_dict[lang]

    nlp.add_pipe("asent_" + lang + "_v1", config={"force": True})

    docs = [nlp(e) for e in [example, more_positive_example]]
    assert docs[0]._.polarity.compound < docs[1]._.polarity.compound


@pytest.mark.parametrize(
    ("example", "expected", "lang"),
    [
        ("I am happy", "positive", "en"),
        ("I am very happy", "positive", "en"),
        ("I am VERY happy", "positive", "en"),
        ("I am not very happy", "negative", "en"),
        ("jeg er glad", "positive", "da"),
        ("jeg er glad", "positive", "no"),
        ("jag är glad", "positive", "sv"),
        ("", "neutral", "da"),
    ],
)
def test_components(example: str, expected: str, lang: str, nlp_dict: dict):
    nlp = nlp_dict[lang]

    nlp.add_pipe("asent_" + lang + "_v1", config={"force": True})
    doc = nlp(example)
    if expected == "positive":
        assert doc._.polarity.compound > 0
    elif expected == "neutral":
        assert doc._.polarity.compound == 0
    elif expected == "negative":
        assert doc._.polarity.compound < 0
    else:
        raise ValueError(
            "Invalid expected value '{expected}', should be either 'neutral', "
            + "'positive' or 'negative'",
        )
