import asent
import pytest

from .test_getters import nlp_dict  # noqa


@pytest.mark.parametrize(
    ("example", "lang"),
    [
        ("I am not very happy", "en"),
        ("jeg er glad", "da"),
        ("jeg er GLAD", "da"),
        ("jeg er MEGET glad", "da"),
        ("jeg er sur", "da"),
        ("jeg er ikke sur", "da"),
        ("jeg er ikke længere sur", "da"),
        ("jeg er ikke længere særligt sur", "da"),
    ],
)
def test_visualize(example: str, lang: str, nlp_dict):  # noqa
    nlp = nlp_dict[lang]
    nlp.add_pipe("asent_" + lang + "_v1")

    doc = nlp(example)

    # test on docs
    asent.visualize(doc, style="prediction")
    asent.visualize(doc, style="analysis")

    # test on spans
    asent.visualize(doc[:2], style="prediction")
    asent.visualize(doc[:2], style="prediction-no-overlap")
    asent.visualize(doc[:2], style="analysis")

    # test on polarities
    pol = doc._.polarity
    asent.visualize(pol, style="prediction")
    asent.visualize(pol, style="prediction-no-overlap")
    asent.visualize(pol, style="analysis")

    # test on span polarities
    span_pol = doc[:2]._.polarity
    asent.visualize(span_pol, style="prediction")
    asent.visualize(span_pol, style="prediction-no-overlap")
    asent.visualize(span_pol, style="analysis")

    # error
    with pytest.raises(ValueError):  # noqa
        asent.visualize(doc[:2], style="invalid")
