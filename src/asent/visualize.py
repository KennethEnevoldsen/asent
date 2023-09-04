from distutils.log import warn
from typing import Union

import spacy
from packaging import version
from spacy import displacy
from spacy.tokens import Doc, Span

from asent.data_classes import DocPolarityOutput, SpanPolarityOutput


def make_colors(n: int = 10, cmap: str = "RdYlGn"):
    """A utility function for creating a stepped color gradient."""
    from pylab import cm, matplotlib  # type: ignore

    cmap = cm.get_cmap(cmap, n)  # PiYG

    for i in range(cmap.N):  # type: ignore
        rgba = cmap(i)  # type: ignore
        # rgb2hex accepts rgb or rgba
        yield matplotlib.colors.rgb2hex(rgba)  # type: ignore


def _normalize_doc_input(
    doc: Union[Span, Doc, DocPolarityOutput, SpanPolarityOutput],
) -> tuple[Span, SpanPolarityOutput]:
    if isinstance(doc, Doc):
        span = doc[:]
        pol = span._.polarity
    elif isinstance(doc, DocPolarityOutput):
        pol = doc.as_span_polarity()
        span = pol.span
    elif isinstance(doc, SpanPolarityOutput):
        pol = doc
        span = doc.span
    else:
        span = doc
        # turn span into doc
        pol = span._.polarity

    return span, pol


def visualize_prediction_no_overlap(
    doc: Union[Span, Doc, DocPolarityOutput, SpanPolarityOutput],
    cmap: str = "RdYlGn",
) -> str:
    """Render displaCy visualisation of model prediction of sentiment.

    This visualization is similar to visualize_prediction, but it does not allow
    for overlapping spans.

    Args:
        doc: The span or document you wish to apply the visualizer
            to.
        cmap: The color map derived from matplotlib. Defaults to
            "RdYlGn".

    Returns:
        Rendered HTML markup.
    """

    span, pol = _normalize_doc_input(doc)

    thresholds = [t / 10 for t in range(-50, 51)]
    sentiment_colors = make_colors(n=len(thresholds), cmap=cmap)
    sentiment_color_dict = {str(t): c for c, t in zip(sentiment_colors, thresholds)}

    def __normalize(val: float) -> str:
        return str(max(min(round(val, 1), 5), -5))

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


def visualize_prediction(
    doc: Union[Span, Doc, SpanPolarityOutput, DocPolarityOutput],
    cmap: str = "RdYlGn",
) -> str:
    """Render displaCy visualisation of model prediction of sentiment.

    Args:
        doc: The span or document you wish to apply the visualizer
            to.
        cmap: The color map derived from matplotlib. Defaults to
            "RdYlGn".

    Returns:
        Rendered HTML markup.
    """
    span, pol = _normalize_doc_input(doc)

    thresholds = [t / 10 for t in range(-50, 51)]
    sentiment_colors = make_colors(n=len(thresholds), cmap=cmap)
    sentiment_color_dict = {str(t): c for c, t in zip(sentiment_colors, thresholds)}

    def __normalize(val: float) -> str:
        return str(max(min(round(val, 1), 5), -5))

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


def visualize_analysis(
    doc: Union[Span, Doc, DocPolarityOutput, SpanPolarityOutput],
) -> str:
    """Render displaCy visualisation of model analysis.

    Args:
        doc: The span or document you wish to apply the visualizer
            to.
        cmap: The color map derived from matplotlib. Defaults to
            "RdYlGn".

    Returns:
        Rendered HTML markup.
    """

    span, pol = _normalize_doc_input(doc)

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


def visualize(
    doc: Union[Span, Doc, DocPolarityOutput, SpanPolarityOutput],
    style: str = "prediction",
    cmap: str = "RdYlGn",
) -> str:
    """Render displaCy visualisation of  model prediction of sentiment or
    analysis of sentiment.

    Args:
        doc: The span or document you wish to apply the visualizer
            to.
        style: A string indicating whether it should visualize
            "prediction" or "analysis". "prediction", color codes positive or negative
            spans according to the cmap. "analysis" visualize for each sentimental word
            if it has by negated or intensified a word, and which word.
            If you are looking for the previous visualizer for "prediction", use
            "prediction-no-overlap". Note that this does not allow for overlapping span.
            Thus it can lead to odd results. Defaults to "prediction".
        cmap: The color map derived from matplotlib. Defaults to "RdYlGn".

    Returns:
        Rendered HTML markup.

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

    if style == "prediction" and version.parse(spacy.__version__) < version.parse(  # type: ignore
        "3.3.0",
    ):
        warn(
            "The visualization style 'prediction' is not available for spacy version "
            + "< 3.3.0. Using 'prediction-no-overlap' instead. Note that this does not"
            + "allow for overlapping span.",
        )
        style = "prediction-no-overlap"

    if style.lower() == "prediction":
        return visualize_prediction(doc, cmap=cmap)
    if style.lower() == "prediction-no-overlap":
        return visualize_prediction_no_overlap(doc, cmap=cmap)
    if style.lower() == "analysis":
        return visualize_analysis(doc)
    raise ValueError(
        "Invalid style argument, should be either 'analysis' or 'prediction'",
    )
