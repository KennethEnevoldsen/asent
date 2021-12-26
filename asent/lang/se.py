import codecs
import os
from inspect import getsourcefile

from spacy.language import Language

from ..constants import B_DECR, B_INCR
from ..utils import lexicons
from ..component import Asent


def read_lexicon():
    lexicon_file = os.path.join("..", "lexicons", "se_lexicon_v1.txt")
    _this_module_file_path_ = os.path.abspath(getsourcefile(lambda: 0))
    lexicon_full_filepath = os.path.join(
        os.path.dirname(_this_module_file_path_), lexicon_file
    )
    with codecs.open(lexicon_full_filepath, encoding="utf-8") as f:
        lexicon = {}
        for line in f.read().rstrip("\n").split("\n"):
            if not line:
                continue
            (word, measure) = line.strip().split("\t")[0:2]
            lexicon[word] = float(measure)
    return lexicon


LEXICON = read_lexicon()

NEGATIONS = {
    "inte",
    "varken",
    "aldrig",
    "ingen",
    "nej",
    "ingenting",
    "ingenstans",
    "utan",
    "sällan",
    "trots",
}
BUT_WORDS = {}

INTENSIFIERS = {
    "absolut": B_INCR,
    "otroligt": B_INCR,
    "väldigt": B_INCR,
    "helt": B_INCR,
    "betydande": B_INCR,
    "betydligt": B_INCR,
    "bestämt": B_INCR,
    "djupt": B_INCR,
    "effing": B_INCR,
    "enorm": B_INCR,
    "enormt": B_INCR,
    "framförallt": B_INCR,
    "speciellt": B_INCR,
    "exceptionell": B_INCR,
    "exceptionellt": B_INCR,
    "extrem": B_INCR,
    "extremt": B_INCR,
    "ytterst": B_INCR,
    "fantastiskt": B_INCR,
    "flipping": B_INCR,
    "flippin": B_INCR,
    "frackin": B_INCR,
    "fracking": B_INCR,
    "fricking": B_INCR,
    "frickin": B_INCR,
    "frigging": B_INCR,
    "friggin": B_INCR,
    "fullt": B_INCR,
    "fuckin": B_INCR,
    "fucking": B_INCR,
    "fuggin": B_INCR,
    "fugging": B_INCR,
    "mycket": B_INCR,
    "hella": B_INCR,
    "högt": B_INCR,
    "högst": B_INCR,
    "intensivt": B_INCR,
    "sjukt": B_INCR,
    "mestadels": B_INCR,
    "mer": B_INCR,
    "mest": B_INCR,
    "särskilt": B_INCR,
    "enbart": B_INCR,
    "ganska": B_INCR,
    "anmärkningsvärt": B_INCR,
    "så": B_INCR,
    "väsentligen": B_INCR,
    "genomgående": B_INCR,
    "total": B_INCR,
    "grundligt": B_INCR,
    "totalt": B_INCR,
    "oerhört": B_INCR,
    "uber": B_INCR,
    "ovanligt": B_INCR,
    "nästan": B_DECR,
    "knappt": B_DECR,
    "marginellt": B_DECR,
    "med nöd och näpppe": B_DECR,
    "ungefär": B_DECR,
    "någorlunda": B_DECR,
    "mindre": B_DECR,
    "lite": B_DECR,
    "litet": B_DECR,
    "ibland": B_DECR,
    "stundvis": B_DECR,
    "delvis": B_DECR,
    "sällsynt": B_DECR,
    "då och då": B_DECR,
    "viss": B_DECR,
}

lexicons.register("lexicon_se_v1", func=LEXICON)
lexicons.register("negations_se_v1", func=NEGATIONS)
lexicons.register("intensifiers_se_v1", func=INTENSIFIERS)


@Language.factory("asent_se_v1")
def create_se_sentiment_component(nlp: Language, name: str) -> Language:
    """
    Allows the Swedish sentiment to be added to a spaCy pipe using nlp.add_pipe("asent_se_v1").
    """

    LEXICON.update(LEXICON)

    return Asent(
        nlp,
        name=name,
        lexicon=LEXICON,
        intensifiers=INTENSIFIERS,
        negations=NEGATIONS,
        contrastive_conjugations=set(),
        lowercase=True,
        lemmatize=False,
    )
