"""Test specifically targeted an bugs."""

import asent  # noqa
import spacy


def test_no_negations_and_intensifiers_out_of_sentence():
    """Test that no negations are not found outside the sentence span.

    https://github.com/KennethEnevoldsen/asent/issues/58
    """

    # create spacy pipeline
    nlp = spacy.blank("en")
    nlp.add_pipe("sentencizer")

    nlp.add_pipe("asent_en_v1")

    text = "Would you do that? I would not. Very stupid is what that is."
    doc = nlp(text)
    assert doc[10]._.is_negated is None

    text = "Would you do that? I would not very. Stupid is what that is."
    doc = nlp(text)
    assert doc[10]._.valence == doc[10]._.polarity.polarity
