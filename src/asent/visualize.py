from distutils.log import warn
from typing import Literal, Union

import spacy
from packaging import version
from spacy import displacy
from spacy.tokens import Doc, Span

from asent.data_classes import DocPolarityOutput, SpanPolarityOutput


def make_colors(n: int = 10, cmap: str = "RdYlGn"):  # type: ignore
    """A utility function for creating a stepped color gradient."""
    from pylab import cm, matplotlib  # type: ignore

    _cmap = cm.get_cmap(cmap, n)  # PiYG # type: ignore

    for i in range(_cmap.N):  # type: ignore
        rgba = _cmap(i)  # type: ignore
        # rgb2hex accepts rgb or rgba
        yield matplotlib.colors.rgb2hex(rgba)  # type: ignore


def __normalize(val: float) -> str:
    return str(max(min(round(val, 1), 5), -5))


def _normalize_input_to_span(
    document_obj: Union[Span, Doc, DocPolarityOutput, SpanPolarityOutput],
) -> tuple[Span, SpanPolarityOutput]:
    if isinstance(document_obj, Doc):
        span = document_obj[:]
        pol = span._.polarity
    elif isinstance(document_obj, DocPolarityOutput):
        pol = document_obj.as_span_polarity()
        span = pol.span
    elif isinstance(document_obj, SpanPolarityOutput):
        pol = document_obj
        span = document_obj.span
    else:
        span = document_obj
        # turn span into doc
        pol = span._.polarity

    return span, pol


def visualize_prediction_no_overlap(
    document_obj: Union[Span, Doc, DocPolarityOutput, SpanPolarityOutput],
    cmap: str = "RdYlGn",
) -> str:
    """Render displaCy visualisation of model prediction of sentiment.

    This visualization is similar to visualize_prediction, but it does not allow
    for overlapping spans.

    Args:
        document_obj: The span or document you wish to apply the visualizer
            to.
        cmap: The color map derived from matplotlib. Defaults to
            "RdYlGn".

    Returns:
        Rendered HTML markup.
    """

    span, pol = _normalize_input_to_span(document_obj)

    thresholds = [t / 10 for t in range(-50, 51)]
    sentiment_colors = make_colors(n=len(thresholds), cmap=cmap)
    sentiment_color_dict = {str(t): c for c, t in zip(sentiment_colors, thresholds)}

    t_pols = list(filter(lambda p: p, pol.polarities))

    c_spans = [
        {
            "start": tp.span.doc[tp.span.start].idx - span.doc[span.start].idx,
            "end": tp.span.doc[tp.span.end - 1].idx
            - span.doc[span.start].idx
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
    document_obj: Union[Span, Doc, SpanPolarityOutput, DocPolarityOutput],
    cmap: str = "RdYlGn",
) -> str:
    """Render displaCy visualisation of model prediction of sentiment.

    Args:
        document_obj: The span or document you wish to apply the visualizer to.
        cmap: The color map derived from matplotlib.

    Returns:
        Rendered HTML markup.
    """
    span, pol = _normalize_input_to_span(document_obj)

    thresholds = [t / 10 for t in range(-50, 51)]
    sentiment_colors = make_colors(n=len(thresholds), cmap=cmap)
    sentiment_color_dict = {str(t): c for c, t in zip(sentiment_colors, thresholds)}

    t_pols = list(filter(lambda p: p, pol.polarities))

    c_spans = [
        {
            "start_token": tp.span.start - span.start,
            "end_token": tp.span.end - span.start,
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
    document_obj: Union[Span, Doc, DocPolarityOutput, SpanPolarityOutput],
) -> str:
    """Render displaCy visualisation of model analysis.

    Args:
        document_obj: The span or document you wish to apply the visualizer to.
        cmap: The color map derived from matplotlib.

    Returns:
        Rendered HTML markup.
    """

    span, pol = _normalize_input_to_span(document_obj)

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
                            "start": intens.i - span.start,
                            "end": t.i - span.start,
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


def visualize_sentence_prediction(
    document_obj: Union[Span, Doc, DocPolarityOutput, SpanPolarityOutput],
    cmap: str = "RdYlGn",
) -> str:
    """Render displaCy visualisation of model prediction of sentiment.

    Args:
        document_obj: The span or document you wish to apply the visualizer to.
        cmap: The color map derived from matplotlib.

    Returns:
        Rendered HTML markup.
    """
    span, _ = _normalize_input_to_span(document_obj)
    doc = span.doc
    sents = list(doc.sents)

    thresholds = [t / 10 for t in range(-10, 11)]
    sentiment_colors = make_colors(n=len(thresholds), cmap=cmap)
    sentiment_color_dict = {str(t): c for c, t in zip(sentiment_colors, thresholds)}

    extended_span = doc[sents[0].start : sents[-1].end]
    start_idx = doc[extended_span.start].idx
    c_spans = [
        {
            "start": doc[sent.start].idx - start_idx,
            "end": doc[sent.end - 1].idx - start_idx + len(doc[sent.end - 1].text),
            "label": __normalize(sent._.polarity.compound),
        }
        for sent in span.sents  # type: ignore
    ]

    ex = [
        {
            "text": extended_span.text,
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


def visualize(
    doc: Union[Span, Doc, DocPolarityOutput, SpanPolarityOutput],
    style: Literal[
        "prediction",
        "analysis",
        "prediction-no-overlap",
        "sentence-prediction",
    ] = "prediction",
    cmap: str = "RdYlGn",
) -> str:
    """Render displaCy visualisation of  model prediction of sentiment or
    analysis of sentiment.

    Args:
        doc: The span or document you wish to apply the visualizer to.
        style: A string indicating whether it should visualize
            "prediction" or "analysis".

            - "prediction", color codes positive or negative spans according to the cmap.
            - "analysis" visualize for each sentimental word whether it has been negated or intensified by a word, and which words.
               it also shows the valence of each word, both raw and taking into account negation and intensification.
            - "sentence-prediction", same as "prediction" but for each sentence instead of per. word.

            If you are looking for the previous visualizer for "prediction", use "prediction-no-overlap".
            Note that this does not allow for overlapping spans and thus it can lead to odd results.
        cmap: The color map derived from matplotlib.

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
    style_ = style.lower()

    if style_ == "prediction" and version.parse(spacy.__version__) < version.parse(  # type: ignore
        "3.3.0",
    ):
        warn(
            "The visualization style 'prediction' is not available for spacy version "
            + "< 3.3.0. Using 'prediction-no-overlap' instead. Note that this does not"
            + "allow for overlapping span.",
        )
        style_ = "prediction-no-overlap"

    if style_ == "prediction":
        return visualize_prediction(doc, cmap=cmap)
    if style_ == "prediction-no-overlap":
        return visualize_prediction_no_overlap(doc, cmap=cmap)
    if style_ == "analysis":
        return visualize_analysis(doc)
    if style_ == "sentence-prediction":
        return visualize_sentence_prediction(doc, cmap=cmap)
    raise ValueError("Unknown style argument.")
