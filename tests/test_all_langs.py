import asent
import spacy


def test_all_lang_components():
    """Test that all language components can be loaded and run on a simple text
    snippet."""
    text = "this is a random test string"
    nlp = spacy.blank("xx")  # multilingual pipe

    for comp in asent.components.get_all():
        nlp.add_pipe(comp, config={"force": True})
        nlp.remove_pipe(comp)
        doc = nlp(text)  # noqa
