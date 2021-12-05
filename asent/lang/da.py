import os
from inspect import getsourcefile

from spacy.language import Language

from ..constants import B_INCR
from ..component import Asent
from ..utils import lexicons

from .emoji import LEXICON as E_LEXICON


def read_lexicon():
    lexicon_file = os.path.join("..", "lexicons", "da_lexicon_v1.csv")
    _this_module_file_path_ = os.path.abspath(getsourcefile(lambda: 0))
    lexicon_full_filepath = os.path.join(
        os.path.dirname(_this_module_file_path_), lexicon_file
    )

    with open(lexicon_full_filepath) as f:
        pairs = filter(lambda x: x, f.read().split("\n")[1:])
        lexicon = {
            word: float(rating) for word, rating in map(lambda x: x.split(","), pairs)
        }
    return lexicon


LEXICON = read_lexicon()

NEGATIONS = {"ikke", "ik", "ikk", "ik'", "aldrig", "ingen"}
CONTRASTIVE_CONJ = {"men", "dog"}

INTENSIFIERS = {
    "absolut": B_INCR,
    "vældig": B_INCR,
    "helt": B_INCR,
    "betydende": B_INCR,
    "betydelig": B_INCR,
    "bestemt": B_INCR,
    "enorm": B_INCR,
    "exceptionel": B_INCR,
    "ekseptionel": B_INCR,
    "extrem": B_INCR,
    "yderst": B_INCR,
    "fantastisk": B_INCR,
    "flipping": B_INCR,
    "flippin": B_INCR,
    "frackin": B_INCR,
    "fracking": B_INCR,
    "fricking": B_INCR,
    "frickin": B_INCR,
    "frigging": B_INCR,
    "friggin": B_INCR,
    "fuckin": B_INCR,
    "fucking": B_INCR,
    "fuggin": B_INCR,
    "fugging": B_INCR,
    "hella": B_INCR,
    "intensiv": B_INCR,
    "mest": B_INCR,
    "særskilt": B_INCR,
    "ganske": B_INCR,
    "væsentlig": B_INCR,
    "uber": B_INCR,
    "virkelig": B_INCR,
    "temmelig": 0.1,
    "megen": 0.2,
    "mega": 0.4,
    "lidt": -0.2,
    "ekstrem": 0.4,
    "total": 0.2,
    "utrolig": 0.3,
    "rimelig": 0.1,
    "seriøs": 0.3,
}

lexicons.register("lexicon_da_v1", func=LEXICON)
lexicons.register("negations_da_v1", func=NEGATIONS)
lexicons.register("contrastive_conj_da_v1", func=CONTRASTIVE_CONJ)
lexicons.register("intensifiers_da_v1", func=INTENSIFIERS)


@Language.factory("asent_da_v1", default_config={"force": False})
def create_da_sentiment_component(nlp: Language, name: str,  force: bool) -> Language:
    """
    Allows the Danish sentiment to be added to a spaCy pipe using nlp.add_pipe("asent_da_v1").
    """

    LEXICON.update(E_LEXICON)

    return Asent(
        nlp,
        name=name, 
        lexicon=LEXICON,
        intensifiers=INTENSIFIERS,
        negations=NEGATIONS,
        contrastive_conjugations=CONTRASTIVE_CONJ,
        lowercase=True,
        lemmatize=True,
        force=force
    )
