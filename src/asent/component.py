"""Calculation of various readability metrics."""

from collections.abc import Iterable
from typing import Any

from spacy.language import Language
from spacy.tokens import Doc, Span, Token

from asent.data_classes import DocPolarityOutput
from asent.getters import (
    make_doc_polarity_getter,
    make_intensifier_getter,
    make_is_contrastive_conj_getter,
    make_is_negated_getter,
    make_is_negation_getter,
    make_span_polarity_getter,
    make_token_polarity_getter,
    make_valance_getter,
)


def dynamic_doc_pol_getter(doc: Doc) -> DocPolarityOutput:
    """A dynamic getter for the doc polarity.

    Args:
        doc (Doc): A spaCy document.

    Returns:
        DocPolarityOutput: A data class representing the polarity of a document.
    """
    pol: dict[str, Any] = doc._._polarity
    return DocPolarityOutput.from_dict(pol, doc=doc)


class Asent:
    """SpaCy v.3.0 component for adding an asent sentiment models to `Doc`
    objects.

    Ading the Token extentions 'valence', 'intensifier', 'is_negation',
    'is_negated', 'is_contrastive_conj' and 'polarity' as well as the
    Span and Doc extension 'polarity'.
    """

    def __init__(
        self,
        nlp: Language,  # noqa: ARG002
        lexicon: dict[str, float],
        name: str = "asent",
        intensifiers: dict[str, float] = {},  # noqa
        negations: Iterable[str] = set(),
        contrastive_conjugations: Iterable[str] = set(),
        lowercase: bool = True,
        lemmatize: bool = False,
        force: bool = False,
    ):
        """Initialize component.

        Args:
            nlp: A spaCy language pipeline for which to add the component to
            name: The name of the component
            lexicon: The lexicion used to look up the valence scores of a word.
            intensifiers: A dictionary of intensifiers (e.g. {"very": 0.293}).
                Defaults to {}, indicating no intensifiers is used.
            negations: A list of negations (e..g "not"). Defaults to an empty set
                indicatin no negations will be used.
            contrastive_conjugations: A list of contrastive conjugations (e.g. "but").
                Defaults to empty set indicating no contrastive conjugations will be used.
            lowercase: Should be text be lowercases before looking up in the lexicons?
                Defaults to True.
            lemmatize: Should be text be lemmatized before looking up in the lexicons?
                Defaults to False.
            force: Should existing extensions be overwritten? Defaults to False.
        """
        self.name = name

        if (not Token.has_extension("valence")) or (force is True):
            Token.set_extension(
                "valence",
                getter=make_valance_getter(
                    lexicon=lexicon,
                    lowercase=lowercase,
                    lemmatize=lemmatize,
                ),
                force=force,
            )

        if (not Token.has_extension("intensifier")) or (force is True):
            Token.set_extension(
                "intensifier",
                getter=make_intensifier_getter(
                    intensifiers=intensifiers,
                    lemmatize=lemmatize,
                    lowercase=lowercase,
                ),
                force=force,
            )

        if (not Token.has_extension("is_negation")) or (force is True):
            Token.set_extension(
                "is_negation",
                getter=make_is_negation_getter(
                    negations=negations,
                    lemmatize=lemmatize,
                    lowercase=lowercase,
                ),
                force=force,
            )

        if (not Token.has_extension("is_negated")) or (force is True):
            Token.set_extension(
                "is_negated",
                getter=make_is_negated_getter(),
                force=force,
            )

        if (not Token.has_extension("is_contrastive_conj")) or (force is True):
            Token.set_extension(
                "is_contrastive_conj",
                getter=make_is_contrastive_conj_getter(
                    contrastive_conjugations=contrastive_conjugations,
                    lemmatize=lemmatize,
                    lowercase=lowercase,
                ),
                force=force,
            )

        if (not Token.has_extension("polarity")) or (force is True):
            Token.set_extension(
                "polarity",
                getter=make_token_polarity_getter(
                    valence_getter=None,
                    is_negation_getter=None,
                    intensifier_getter=None,
                ),
                force=force,
            )

        if (not Span.has_extension("polarity")) or (force is True):
            Span.set_extension(
                "polarity",
                getter=make_span_polarity_getter(
                    polarity_getter=None,
                    contrastive_conj_getter=None,
                ),
                force=force,
            )

        if (not Doc.has_extension("_polarity")) or (force is True):
            self.doc_pol_getter = make_doc_polarity_getter(span_polarity_getter=None)
            Doc.set_extension(
                "_polarity",
                default=None,
                force=force,
            )

        if (not Doc.has_extension("polarity")) or (force is True):
            Doc.set_extension(
                "polarity",
                getter=dynamic_doc_pol_getter,
                force=force,
            )

    def __call__(self, doc: Doc) -> Doc:
        """Run the pipeline component.

        Args:
            doc: A spaCy document the component should be applied to.

        Returns:
            A processed spacy Document.
        """
        pol = self.doc_pol_getter(doc)
        doc._._polarity = pol.to_dict()
        return doc


DEFAULT_CONFIG = {
    "lexicon": {},
    "intensifiers": {},
    "negations": set(),
    "contrastive_conj": set(),
    "lowercase": True,
    "lemmatize": False,
    "force": True,
}


@Language.factory("asent_v1", default_config=DEFAULT_CONFIG)
def create_asent_component(
    nlp: Language,
    name: str,
    lexicon: dict[str, float],
    intensifiers: dict[str, float],
    negations: Iterable[str],
    contrastive_conj: Iterable[str],
    lowercase: bool,
    lemmatize: bool,
    force: bool,
) -> Asent:
    """Allows a asent sentiment pipe to be added to a spaCy pipe using
    nlp.add_pipe("asent_v1").

    Args:
        nlp: A spaCy language pipeline to add the component to.
        name: The name of the component.
        lexicon: The lexicion used to look up the valence scores of a word.
        intensifiers: A dictionary of intensifiers (e.g. {"very": 0.293}).
        negations: A list of negations (e.g. "not").
        contrastive_conj: A list of contrastive conjugations (e.g. "but").
        lowercase: Should be text be lowercases before looking up in the lexicons?
        lemmatize: Should be text be lemmatized before looking up in the lexicons?
        force: Should existing extensions be overwritten?

    Returns:
        A sentiment component.
    """

    return Asent(
        nlp,
        name=name,
        lexicon=lexicon,
        intensifiers=intensifiers,
        negations=negations,
        contrastive_conjugations=contrastive_conj,
        lowercase=lowercase,
        lemmatize=lemmatize,
        force=force,
    )
