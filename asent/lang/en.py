import codecs
import os
from inspect import getsourcefile

from spacy.language import Language

from ..constants import B_DECR, B_INCR
from ..utils import lexicons
from..component import Asent

from .emoji import LEXICON as E_LEXICON

def read_lexicon():
    lexicon_file = os.path.join("..", "lexicons", "en_lexicon_v1.txt")
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
    "aint",
    "arent",
    "cannot",
    "cant",
    "couldnt",
    "darent",
    "didnt",
    "doesnt",
    "ain't",
    "aren't",
    "can't",
    "couldn't",
    "daren't",
    "didn't",
    "doesn't",
    "dont",
    "hadnt",
    "hasnt",
    "havent",
    "isnt",
    "mightnt",
    "mustnt",
    "neither",
    "don't",
    "hadn't",
    "hasn't",
    "haven't",
    "isn't",
    "mightn't",
    "mustn't",
    "neednt",
    "needn't",
    "never",
    "none",
    "nope",
    "nor",
    "not",
    "nothing",
    "nowhere",
    "oughtnt",
    "shant",
    "shouldnt",
    "uhuh",
    "wasnt",
    "werent",
    "oughtn't",
    "shan't",
    "shouldn't",
    "uh-uh",
    "wasn't",
    "weren't",
    "without",
    "wont",
    "wouldnt",
    "won't",
    "wouldn't",
    "rarely",
    "seldom",
    "despite",
}

CONTRASTIVE_CONJ = {"but"}

INTENSIFIERS = {
    "absolutely": B_INCR,
    "amazingly": B_INCR,
    "awfully": B_INCR,
    "completely": B_INCR,
    "considerable": B_INCR,
    "considerably": B_INCR,
    "decidedly": B_INCR,
    "deeply": B_INCR,
    "effing": B_INCR,
    "enormous": B_INCR,
    "enormously": B_INCR,
    "entirely": B_INCR,
    "especially": B_INCR,
    "exceptional": B_INCR,
    "exceptionally": B_INCR,
    "extreme": B_INCR,
    "extremely": B_INCR,
    "fabulously": B_INCR,
    "flipping": B_INCR,
    "flippin": B_INCR,
    "frackin": B_INCR,
    "fracking": B_INCR,
    "fricking": B_INCR,
    "frickin": B_INCR,
    "frigging": B_INCR,
    "friggin": B_INCR,
    "fully": B_INCR,
    "fuckin": B_INCR,
    "fucking": B_INCR,
    "fuggin": B_INCR,
    "fugging": B_INCR,
    "greatly": B_INCR,
    "hella": B_INCR,
    "highly": B_INCR,
    "hugely": B_INCR,
    "incredible": B_INCR,
    "incredibly": B_INCR,
    "intensely": B_INCR,
    "major": B_INCR,
    "majorly": B_INCR,
    "more": B_INCR,
    "most": B_INCR,
    "particularly": B_INCR,
    "purely": B_INCR,
    "quite": B_INCR,
    "really": B_INCR,
    "remarkably": B_INCR,
    "so": B_INCR,
    "substantially": B_INCR,
    "thoroughly": B_INCR,
    "total": B_INCR,
    "totally": B_INCR,
    "tremendous": B_INCR,
    "tremendously": B_INCR,
    "uber": B_INCR,
    "unbelievably": B_INCR,
    "unusually": B_INCR,
    "utter": B_INCR,
    "utterly": B_INCR,
    "very": B_INCR,
    "almost": B_DECR,
    "barely": B_DECR,
    "hardly": B_DECR,
    "just enough": B_DECR,
    "kind of": B_DECR,
    "kinda": B_DECR,
    "kindof": B_DECR,
    "kind-of": B_DECR,
    "less": B_DECR,
    "little": B_DECR,
    "marginal": B_DECR,
    "marginally": B_DECR,
    "occasional": B_DECR,
    "occasionally": B_DECR,
    "partly": B_DECR,
    "scarce": B_DECR,
    "scarcely": B_DECR,
    "slight": B_DECR,
    "slightly": B_DECR,
    "somewhat": B_DECR,
    "sort of": B_DECR,
    "sorta": B_DECR,
    "sortof": B_DECR,
    "sort-of": B_DECR,
}

lexicons.register("lexicon_en_v1", func=LEXICON)
lexicons.register("negations_en_v1", func=NEGATIONS)
lexicons.register("contrastive_conj_en_v1", func=CONTRASTIVE_CONJ)
lexicons.register("intensifiers_en_v1", func=INTENSIFIERS)

@Language.factory("asent_en_v1")
def create_en_sentiment_component(nlp: Language, name: str) -> Language:
    """
    Allows the English sentiment to be added to a spaCy pipe using nlp.add_pipe("asent_en_v1").
    """
    LEXICON.update(E_LEXICON)

    return Asent(nlp, 
        lexicon = LEXICON,
        intensifiers = INTENSIFIERS,
        negations = NEGATIONS,
        contrastive_conjugations = CONTRASTIVE_CONJ,
        lowercase =True,
        lemmatize =False)