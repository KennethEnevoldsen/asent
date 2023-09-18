import asent
import spacy
from asent.data_classes import DocPolarityOutput


def test_all_lang_components():
    """Test that all language components can be loaded and run on a simple text
    snippet."""
    text = "this is a random test string"
    nlp = spacy.blank("xx")  # multilingual pipe

    for comp in asent.components.get_all():
        nlp.add_pipe(comp, config={"force": True})
        nlp.remove_pipe(comp)
        nlp(text)


def test_multiprocessing():
    documents = ["I am happy", "I am sad"]

    model = spacy.blank("en")
    model.add_pipe("sentencizer", first=True)
    model.add_pipe("asent_en_v1")

    for doc in model.pipe(documents, batch_size=16, n_process=2):
        assert isinstance(doc._.polarity, DocPolarityOutput)
