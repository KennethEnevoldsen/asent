"""Calculation of various readability metrics."""

from spacy.tokens import Token, Doc, Span
from spacy.language import Language

from typing import Dict, Iterable


from asent.getters import (
    make_token_polarity_getter,
    make_span_polarity_getter,
    make_is_negation_getter,
    make_valance_getter,
    make_intensifier_getter,
    make_is_contrastive_conj_getter,
    make_doc_polarity_getter,
)


class Asent:
    """spaCy v.3.0 component for adding an asent sentiment models to `Doc` objects.
    Ading the Token extentions valence, intensifier, is_negation, is_contrastive_conj,
    and polarity as well as the Span and Doc extensions polarity.
    """

    def __init__(
        self,
        nlp: Language,
        lexicon: Dict[str, float],
        intensifiers: Dict[str, float] = {},
        negations: Iterable[str] = set(),
        contrastive_conjugations: Iterable[str] = set(),
        lowercase: bool = True,
        lemmatize: bool = True,
        force: bool=False,
    ):
        """Initialise components"""

        if (not Token.has_extension("valence")) or (force is True):
            Token.set_extension(
                "valence",
                getter=make_valance_getter(lexicon=lexicon, lowercase=lowercase, lemmatize=lemmatize),
                force=force
            )

        if (not Token.has_extension("intensifier")) or (force is True):
            Token.set_extension(
                "intensifier",
                getter=make_intensifier_getter(intensifiers=intensifiers, lemmatize=lemmatize, lowercase=lowercase),
                force=force
            )

        if (not Token.has_extension("is_negation")) or (force is True):
            Token.set_extension(
                "is_negation",
                getter=make_is_negation_getter(negations=negations, lemmatize=lemmatize, lowercase=lowercase),
                force=force
            )

        if (not Token.has_extension("is_contrastive_conj")) or (force is True):
            Token.set_extension(
                "is_contrastive_conj",
                getter=make_is_contrastive_conj_getter(
                    contrastive_conjugations=contrastive_conjugations,
                    lemmatize=lemmatize, lowercase=lowercase
                ),
                force=force
            )

        if (not Token.has_extension("polarity")) or (force is True):
            Token.set_extension(
                "polarity",
                getter=make_token_polarity_getter(
                    valence_getter=None, is_negation_getter=None, intensifier_getter=None,
                ),
                force=force
            )

        if (not Span.has_extension("polarity")) or (force is True):
            Span.set_extension(
                "polarity",
                getter=make_span_polarity_getter(
                    polarity_getter=None, contrastive_conj_getter=None,

                ),
                force=force
            )

        if (not Doc.has_extension("polarity")) or (force is True):
            Doc.set_extension(
                "polarity",
                getter=make_doc_polarity_getter(span_polarity_getter=None),
                force=force
            )


    def __call__(self, doc: Doc):
        """Run the pipeline component"""
        return doc

