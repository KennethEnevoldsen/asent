# pos/neg words
# boosters
# caps
# negations
# idioms
# emoticons
# exclamation questionmarks amplyfication

# pos, neg, neu

from typing import Iterable
from spacy.tokens import Token
from spacy import displacy




# import spacy

# nlp = spacy.load("da_core_news_sm")
# doc = nlp("jeg er så glad")

# doc[0]._.sentiment


# ex = [
#     {
#         "text": "But Google is starting from behind.",
#         "ents": [{"start": 4, "end": 10, "label": "ORG"}],
#         "title": None,
#     }
# ]
# displacy.render(ex, style="ent", manual=True)


# import spacy
# from spacy import displacy

# nlp = spacy.load("en_core_web_sm")
# doc = nlp("My name is Kenneth")
# html = displacy.render(doc, style="ent")


# colors = {
#     "0": "#fdfebc",
#     "1": "#ffeda0",
#     "2": "#fed976",
#     "3": "#feb24c",
#     "4": "#fd8d3c",
#     "5": "#fc4e2a",
#     "6": "#e31a1c",
#     "7": "#bd0026",
# }

# TPL_TOK = """
# <mark class="entity" style="background: {bg}; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em; box-decoration-break: clone; -webkit-box-decoration-break: clone">
#     {text}
# </mark>
# """
# ex = [
#     {
#         "text": "But Google is starting from behind.",
#         "ents": [
#             {"start": 1, "end": 5, "label": "2"},
#             {"start": 4, "end": 15, "label": "0"},
#         ],
#         "title": None,
#     }
# ]
# html = displacy.render(
#     ex, style="ent", manual=True, options={"colors": colors, "template": TPL_TOK}
# )


def make_colors(n=10, cmap="RdYlGn"):
    from pylab import cm, matplotlib

    cmap = cm.get_cmap(cmap, n)  # PiYG

    for i in range(cmap.N):
        rgba = cmap(i)
        # rgb2hex accepts rgb or rgba
        yield matplotlib.colors.rgb2hex(rgba)


def print_colors(HEX: Iterable) -> None:
    from IPython.core.display import HTML, display

    for color in HEX:
        display(HTML(f'<p style="color:{color}">{color}</p>'))




########
########
########

import spacy
from spacy.tokens import Span
from spacy import displacy


from sentida.getters import make_span_polarity_getter

Span.set_extension(
    "polarity",
    getter=make_span_polarity_getter(),
)

text = "jeg er ikke længere sur"
nlp = spacy.load("da_core_news_lg")
doc = nlp(text)
sent = [sent for sent in doc.sents][0]
sent._.polarity
span = sent



TPL_TOK = """
<mark class="entity" style="background: {bg}; 
padding: 0.45em 0.6em; margin: 0 0.25em; 
line-height: 1; border-radius: 0.35em; 
box-decoration-break: clone; 
-webkit-box-decoration-break: clone">
    {text}
</mark>
"""

def dacy_displacy(span: Span, style="polarity"):
    thresholds = [t / 10 for t in range(-50, 51)]
    sentiment_colors = make_colors(n=len(thresholds))
    sentiment_color_dict = {str(t): c for c, t in zip(sentiment_colors, thresholds)}

    def __normalize(val: float) -> str:
        return str(max(min(round(val, 1), 5), -5))

    pol = span._.polarity
    t_pols = list(filter(lambda p: p, pol.polarities))
    
    c_spans = [
        {"start": tp.span.doc[tp.span.start].idx - span.doc[span.start].idx, "end": tp.span.doc[tp.span.end-1].idx + len(tp.span.doc[tp.span.end-1].text), "label": __normalize(tp.polarity)}
        for tp in t_pols
    ]

    ex = [
        {
            "text": span.text,
            "ents": c_spans,
            "title": None,
        }
    ]
    html = displacy.render(
        ex, style="ent", manual=True, options={"colors": sentiment_color_dict}
    )
    return html

text = """
Israel truer med landoffensiv i Gaza: 'De har endnu ikke opnået, hvad de ville'

Israel og Hamas har igen i dag affyret raketter og missiler mod hinanden.


Indbyggerne i Israel og Gaza lever torsdag aften fortsat i akut fare.
Dødstallene stiger fortsat dag for dag. I skrivende stund er 83 blevet dræbt i Gaza og syv i Israel. Som om luftbombardementerne ikke var nok, risikerer den militante konflikt nu også at tage form på landjorden.
I løbet af dagen har Israel nemlig sendt 9.000 soldater til grænseområdet langs Gazastriben. Og israelerne lægger ikke skjul på, at en landoffensiv så absolut er på tegnebrættet. Det fortæller mellemøstkorrespondent for Kristeligt Dagblad, Allan Sørensen, til DR fra Tel Aviv.
- Spørgsmålet er, om det er et taktisk spil overfor Hamas, så man kan få dem til at bede om en våbenhvile, eller om Israel faktisk mener det.
Ifølge Allan Sørensen vil mange israelere bakke op om en fortsættelse af kampene, siger han.
- Mange spørger sig selv, hvorfor man skulle stoppe offensiven nu. Hvis Israel stopper, vil man stå med en fornemmelse af, at man ikke har opnået, hvad man ville. Og derfor mener mange, at det er tid til at få det her afgjort en gang for alle, siger Allan Sørensen.

Et hjem kan pludselig blive en grav
Konflikten har ulmet i flere uger, siden midten af april, hvor israelsk politi gentagne gange er stødt sammen med palæstinensere i det østlige Jerusalem.
Kampene foregår ikke bare mellem væbnede, militante styrker på begge sider af konflikten. I flere israelske byer er israelske jøder og israelske arabere stødt sammen i svære voldsudgydelser.

Flere internationale medier beskriver nu situationen, som den voldeligste i området siden 2014. På begge sider sætter frygten blandt indbyggerne sit tydelige spor:
- Jeg kan ikke sove. Hver eneste øjeblik kan dit hjem blive din grav, siger Najwa Sheikh-Ahmad, der bor i Gaza:
- Man kan ikke føle sig sikker. Som mor er det frygteligt, og jeg er fuldstændig udmattet. Følelsesmæssigt og menneskeligt, siger hun til BBC.
I dag blev flere ledere fra Hamas-bevægelsen begravet i Gaza. Organisationen bekræftede i går, at flere militære ledere blev dræbt i et luftangreb.

Flyafgange aflyses
Ifølge Israels militær har Hamas, der figurerer på EU's terrorliste, sendt yderligere 160 missiler mod Israel siden klokken syv i morges. Ifølge militæret er store dele af missilerne blevet tilintetgjort af Israels anti-missilsystem ved navn Iron Dome.
Israel har da heller ikke holdt sig tilbage og har ifølge militæret i dag forsøgt at ramme banker og efterretningskontorer i Gaza.
Fly på vej til lufthavnen Ben Gurion nær Tel Aviv sendes nu i stedet syd på til lufthavnen Ramon. Og flere selskaber har helt valgt at aflyse alle afgange til Israel.
FN har flere gange advaret, at konflikten risikerer at ende i en decideret krig.
- Situationen udvikler sig til krig for fuld udblæsning. Ledere på alle sider er nødt til at tage ansvar for at nedtrappe konflikten, sagde FN's udsending i Mellemøsten, Tor Wennesland, i går.
"""
nlp = spacy.load("da_core_news_lg")
doc = nlp(text)
sents = [sent for sent in doc.sents]
span = doc[0:]
# displacy.render(doc)


dacy_displacy(doc[0:])
