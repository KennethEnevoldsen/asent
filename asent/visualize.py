from typing import Iterable, Union
from spacy.tokens import Span, Doc
from spacy import displacy

def visualize(span: Union[Span, Doc], cmap="RdYlGn"):
    if isinstance(span, Doc):
        span = span[:]
    thresholds = [t / 10 for t in range(-50, 51)]
    sentiment_colors = make_colors(n=len(thresholds), cmap=cmap)
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