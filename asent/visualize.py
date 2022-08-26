from typing import Union

from spacy import displacy
from spacy.tokens import Doc, Span


def visualize(doc: Union[Span, Doc], style: str = "prediction", cmap="RdYlGn") -> str:
    """Render displaCy visualisation of  model prediction of sentiment or
    analysis of sentiment.

    Args:
        doc (Union[Span, Doc]): The span or document you wish to apply the visualizer to.
        style (str): A string indicating whether it should visualize
            "prediction" or "analysis". "prediction", color codes positive or negative
            spans according to the cmap. "analysis" visualize for each sentimental word
            if it has by negated or intensified a word, and which word.
            If you are looking for the previous visualizer for "prediction", use
            "prediction-no-overlap". Note that this does not allow for overlapping span.
            Thus it can lead to odd results. Defaults to "prediction".
        cmap (str): The color map derived from matplotlib. Defaults to "RdYlGn".

    Returns:
        str: Rendered HTML markup.

    Examples:
        >>> nlp = spacy.load("en_core_web_lg")
        >>> # add the rule-based sentiment model
        >>> nlp.add_pipe("asent_en_v1")
        >>> # try an example
        >>> text = "I am not very happy"
        >>> doc = nlp(text)
        >>> # visualize model prediction
        >>> asent.visualize(doc, style="prediction")
        >>> asent.visualize(doc, style="analysis")
    """
    if style.lower() == "prediction":
        return visualize_prediction(doc, cmap=cmap)
    elif style.lower() == "prediction-no-overlap":
        return visualize_prediction_no_overlap(doc, cmap=cmap)
    elif style.lower() == "analysis":
        return visualize_analysis(doc)
    else:
        raise ValueError(
            "Invalid style argument, should be either 'analysis' or 'prediction'",
        )


def visualize_prediction_no_overlap(doc: Union[Span, Doc], cmap="RdYlGn") -> str:
    """Render displaCy visualisation of model prediction of sentiment.

    This visualization is similar to visualize_prediction, but it does not allow
    for overlapping spans.

    Args:
        doc (Union[Span, Doc]): The span or document you wish to apply the visualizer to.
        cmap (str, optional): The color map derived from matplotlib. Defaults to "RdYlGn".

    Returns:
        str: Rendered HTML markup.
    """

    if isinstance(doc, Doc):
        span = doc[:]
    else:
        span = doc

    thresholds = [t / 10 for t in range(-50, 51)]
    sentiment_colors = make_colors(n=len(thresholds), cmap=cmap)
    sentiment_color_dict = {str(t): c for c, t in zip(sentiment_colors, thresholds)}

    def __normalize(val: float) -> str:
        return str(max(min(round(val, 1), 5), -5))

    pol = span._.polarity
    t_pols = list(filter(lambda p: p, pol.polarities))

    c_spans = [
        {
            "start": tp.span.doc[tp.span.start].idx - span.doc[span.start].idx,
            "end": tp.span.doc[tp.span.end - 1].idx
            + len(tp.span.doc[tp.span.end - 1].text),
            "label": __normalize(tp.polarity),
        }
        for tp in t_pols
    ]

    ex = [
        {
            "text": span.text,
            "ents": c_spans,
            "title": None,
        },
    ]

    html = displacy.render(
        ex,
        style="ent",
        manual=True,
        options={"colors": sentiment_color_dict},
    )
    return html


def visualize_prediction(doc: Union[Span, Doc], cmap="RdYlGn") -> str:
    """Render displaCy visualisation of model prediction of sentiment.

    Args:
        doc (Union[Span, Doc]): The span or document you wish to apply the visualizer to.
        cmap (str, optional): The color map derived from matplotlib. Defaults to "RdYlGn".

    Returns:
        str: Rendered HTML markup.
    """

    if isinstance(doc, Doc):
        span = doc[:]
    else:
        span = doc

    thresholds = [t / 10 for t in range(-50, 51)]
    sentiment_colors = make_colors(n=len(thresholds), cmap=cmap)
    sentiment_color_dict = {str(t): c for c, t in zip(sentiment_colors, thresholds)}

    def __normalize(val: float) -> str:
        return str(max(min(round(val, 1), 5), -5))

    pol = span._.polarity
    t_pols = list(filter(lambda p: p, pol.polarities))

    c_spans = [
        {
            "start_token": tp.span.start,
            "end_token": tp.span.end,
            "label": __normalize(tp.polarity),
        }
        for tp in t_pols
    ]
    ex = [
        {
            "text": span.text,
            "spans": c_spans,
            "tokens": [t.text for t in span],
        },
    ]

    html = displacy.render(
        ex,
        style="span",
        manual=True,
        options={"colors": sentiment_color_dict},
    )

    return html


def visualize_analysis(doc: Union[Span, Doc]) -> str:
    """Render displaCy visualisation of model analysis.

    Args:
        doc (Union[Span, Doc]): The span or document you wish to apply the visualizer to.

    Returns:
        str: Rendered HTML markup.
    """

    if isinstance(doc, Doc):
        span = doc[:]
    else:
        span = doc

    pol = span._.polarity

    arcs = []
    words = []
    for t, t_pol in zip(span, pol.polarities):
        if t._.valence:
            words.append(
                {
                    "text": t.text,
                    "tag": f"{t._.polarity.polarity:.1f} ({t._.valence:.1f})",
                },
            )
        else:
            words.append({"text": t.text, "tag": f"{t._.valence:.1f}"})

        if t_pol:
            if t_pol.intensifiers:
                for intens in t_pol.intensifiers:
                    arcs.append(
                        {
                            "start": intens.i,
                            "end": t.i,
                            "label": "intensified by",
                            "dir": "left",
                        },
                    )
            if t_pol.negation:
                arcs.append(
                    {
                        "start": t_pol.negation.i,
                        "end": t.i,
                        "label": "negated by",
                        "dir": "left",
                    },
                )
    # Visualize analysis
    from spacy import displacy

    ex = {"words": words, "arcs": arcs}
    html = displacy.render(ex, style="dep", manual=True)

    return html


def make_colors(n=10, cmap="RdYlGn"):
    """A utility function for creating a stepped color gradient."""
    from pylab import cm, matplotlib

    cmap = cm.get_cmap(cmap, n)  # PiYG

    for i in range(cmap.N):
        rgba = cmap(i)
        # rgb2hex accepts rgb or rgba
        yield matplotlib.colors.rgb2hex(rgba)


# def print_colors(HEX: Iterable) -> None:
#     """An utility function for visualizing a color map"""
#     from IPython.core.display import HTML, display

#     for color in HEX:
#         display(HTML(f'<p style="color:{color}">{color}</p>'))
