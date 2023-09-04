from spacy.language import Language

from ..component import Asent
from ..constants import B_DECR, B_INCR
from ..utils import LEXICON_PATH, components, lexicons, read_lexicon

LANG = "sv"
LEXICON = read_lexicon(LEXICON_PATH / f"{LANG}_lexicon_v1.txt")
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
CONTRASTIVE_CONJ: set[str] = set()
INTENSIFIERS: dict[str, float] = {
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

lexicons.register(f"lexicon_{LANG}_v1", func=LEXICON)
lexicons.register(f"negations_{LANG}_v1", func=NEGATIONS)
lexicons.register(f"intensifiers_{LANG}_v1", func=INTENSIFIERS)


@Language.factory(f"asent_{LANG}_v1", default_config={"force": True})
def create_sv_sentiment_component(nlp: Language, name: str, force: bool) -> Asent:
    """Allows the Swedish sentiment to be added to a spaCy pipe using
    nlp.add_pipe("asent_sv_v1")."""

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
        force=force,
    )


components.register(f"asent_{LANG}_v1", func=create_sv_sentiment_component)
