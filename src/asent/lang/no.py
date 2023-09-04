from spacy.language import Language

from ..component import Asent
from ..utils import LEXICON_PATH, components, lexicons, read_lexicon
from .emoji import LEXICON as E_LEXICON

LANG = "no"
LEXICON = read_lexicon(LEXICON_PATH / "no_lexicon_v1.txt")
NEGATIONS = {"ikke", "ik", "ikk", "ik'", "aldrig", "ingen"}
CONTRASTIVE_CONJ = {"dog", "men"}
INTENSIFIERS = {
    "Temmelig ": 0.293,  # bokmål
    "Meget ": 0.293,
    "Mega": 0.293,
    "Litt": 0.293,
    "Ekstremt": 0.293,
    "Totalt": 0.293,
    "Utrolig": 0.293,
    "Veldig ": 0.293,
    "Bestemt": 0.293,
    "Seriøst": 0.293,
    "Absolutt ": 0.293,
    "Helt": 0.293,
    "Betydelig": 0.293,
    "Dypt": 0.293,
    "Djupt": 0.293,
    "Effing": 0.293,
    "Effin": 0.293,
    "Enormt": 0.293,
    "Fremfor alt": 0.293,
    "Spesiell": 0.293,
    "Eksepsjonelt": 0.293,
    "Ytterst": 0.293,
    "Fantastisk": 0.293,
    "Flipping": 0.293,
    "Flippin": 0.293,
    "Frackin": 0.293,
    "Fracking": 0.293,
    "Frickin": 0.293,
    "Fricking": 0.293,
    "Friggin": 0.293,
    "Frigging": 0.293,
    "Fuckin": 0.293,
    "Fucking": 0.293,
    "Fuggin": 0.293,
    "Fugging": 0.293,
    "Hella": 0.293,
    "Høyt": 0.293,
    "Fullt ": 0.293,
    "Høyst": 0.293,
    "Særdeles": 0.293,
    "Intenst": 0.293,
    "Intensivt": 0.293,
    "Sykt": 0.293,
    "Mer": 0.293,
    "Mest": 0.293,
    "Særlig": 0.293,
    "Ganske": 0.293,
    "Bemerkelsesverdig": 0.293,
    "Bare": 0.293,
    "Så": 0.293,
    "Vesentlig": 0.293,
    "Gjennomgående": 0.293,
    "Grundig": 0.293,
    "Svært": 0.293,
    "Uber": 0.293,
    "Uvanlig": 0.293,
    "Mye": 0.293,
    "Maskimalt": 0.293,
    "Nesten": -0.293,
    "Knapt": -0.293,
    "Marginalt": -0.293,
    "Med nød og neppe ": -0.293,
    "Så vidt": -0.293,
    "Omtrent": -0.293,
    "Noenlunde": -0.293,
    "Mindre": -0.293,
    "Lite": -0.293,
    "Iblant": -0.293,
    "Delvis": -0.293,
    "Sjelden": -0.293,
    "Sjelden(t)": -0.293,
    "Nå og da": -0.293,
    "Av og til": -0.293,
    "Vist": -0.293,
    "Mykje": 0.293,  # nynorsk
    "Utruleg": 0.293,
    "Bestemd": 0.293,
    "Heilt": 0.293,
    "Betydeleg": 0.293,
    "Framfor alt": 0.293,
    "Uvanleg": 0.293,
    "Yttarst": 0.293,
    "Høgt": 0.293,
    "Høgst": 0.293,
    "Særs": 0.293,
    "Serdeles": 0.293,
    "Sers": 0.293,
    "Sjukt": 0.293,
    "Meir": 0.293,
    "Særleg": 0.293,
    "Usadvenleg": 0.293,
    "Utpreget": 0.293,
    "Ekstra": 0.293,
    "Berre": 0.293,
    "Vesentleg": 0.293,
    "Gjennomgåande": 0.293,
    "Sværande": 0.293,
    "Noko": -0.293,
    "So vidt": -0.293,
    "Nokoleis": -0.293,
    "Nokolunde": -0.293,
    "Sjeldan": -0.293,
    "No og da": -0.293,
}

lexicons.register(f"lexicon_{LANG}_v1", func=LEXICON)
lexicons.register(f"negations_{LANG}_v1", func=NEGATIONS)
lexicons.register(f"contrastive_conj_{LANG}_v1", func=CONTRASTIVE_CONJ)
lexicons.register(f"intensifiers_{LANG}_v1", func=INTENSIFIERS)


@Language.factory(f"asent_{LANG}_v1", default_config={"force": True})
def create_no_sentiment_component(nlp: Language, name: str, force: bool) -> Asent:
    """Allows the Norwegian sentiment to be added to a spaCy pipe using
    nlp.add_pipe("asent_no_v1")."""

    LEXICON.update(E_LEXICON)

    return Asent(
        nlp,
        name=name,
        lexicon=LEXICON,
        intensifiers=INTENSIFIERS,
        negations=NEGATIONS,
        contrastive_conjugations=CONTRASTIVE_CONJ,
        lowercase=True,
        lemmatize=False,
        force=force,
    )


components.register(f"asent_{LANG}_v1", func=create_no_sentiment_component)
