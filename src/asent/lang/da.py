from spacy.language import Language

from ..component import Asent
from ..constants import B_INCR
from ..utils import LEXICON_PATH, components, lexicons, read_lexicon
from .emoji import LEXICON as E_LEXICON

LANG = "da"


def read_csv_lexicon() -> dict[str, float]:
    lexicon_file = LEXICON_PATH / f"{LANG}_lexicon_sentida_lemma_v1.csv"

    with open(lexicon_file, encoding="utf-8") as f:  # noqa
        pairs = filter(lambda x: x, f.read().split("\n")[1:])
        lexicon = {
            word: float(rating) for word, rating in (x.split(",") for x in pairs)
        }
    return lexicon


LEXICON = read_csv_lexicon()
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
    "særlig": B_INCR,
    "særligt": B_INCR,
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


lexicons.register(f"lexicon_{LANG}_sentida_lemma_v1", func=LEXICON)
lexicons.register(f"negations_{LANG}_v1", func=NEGATIONS)
lexicons.register(f"contrastive_conj_{LANG}_v1", func=CONTRASTIVE_CONJ)
lexicons.register(f"intensifiers_{LANG}_v1", func=INTENSIFIERS)

lexicons.register(
    "lexicon_da_afinn_v1",
    func=read_lexicon(LEXICON_PATH / f"{LANG}_lexicon_afinn_v1.txt"),
)
lexicons.register(  # store as default
    f"lexicon_{LANG}_v1",
    func=lexicons.get(f"lexicon_{LANG}_afinn_v1"),
)


@Language.factory(f"asent_{LANG}_v1", default_config={"force": True})
def create_da_sentiment_component(nlp: Language, name: str, force: bool) -> Asent:
    """Allows the Danish sentiment to be added to a spaCy pipe using
    nlp.add_pipe("asent_da_v1")."""

    lex = lexicons.get(f"lexicon_{LANG}_afinn_v1")
    lex.update(E_LEXICON)

    return Asent(
        nlp,
        name=name,
        lexicon=lex,
        intensifiers=INTENSIFIERS,
        negations=NEGATIONS,
        contrastive_conjugations=CONTRASTIVE_CONJ,
        lowercase=True,
        lemmatize=False,
        force=force,
    )


components.register(f"asent_{LANG}_v1", func=create_da_sentiment_component)
