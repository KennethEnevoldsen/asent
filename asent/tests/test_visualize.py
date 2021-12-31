import asent
import pytest

from .test_getters import nlp_dict


@pytest.mark.parametrize(
    "example,lang",
    [
        ("jeg er glad", "da"),
        ("jeg er GLAD", "da"),
        ("jeg er sur", "da"),
        ("jeg er ikke sur", "da"),
        ("jeg er ikke længere sur", "da"),
        ("jeg er ikke længere særligt sur", "da"),
    ],
)
def test_visualize(example: str, lang: str, nlp_dict):

    nlp = nlp_dict[lang]
    nlp.add_pipe("asent_" + lang + "_v1")

    doc = nlp(example)
    asent.visualize(doc, style="prediction")
    asent.visualize(doc, style="analysis")
