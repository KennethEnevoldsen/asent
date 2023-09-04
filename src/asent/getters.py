import math
from collections.abc import Iterable
from typing import Callable, Optional, Union

from spacy.tokens import Doc, Span, Token

from .constants import AFTER_BUT_SCALAR, BEFORE_BUT_SCALAR, C_INCR, N_SCALAR
from .data_classes import DocPolarityOutput, SpanPolarityOutput, TokenPolarityOutput


def make_txt_getter(lemmatize: bool, lowercase: bool) -> Callable[[Token], str]:
    """Creates a token getter which return the string of a text string.

    Args:
        lemmatize (bool): Should the token be lemmatized?
        lowercase (bool): Should the token be lowercased?

    Returns:
        Callable[[Token], str]: The getter function
    """

    def get_lower_lemma(token: Token) -> str:
        return token.lemma_.lower()

    def get_lemma(token: Token) -> str:
        return token.lemma_

    def get_lower_txt(token: Token) -> str:
        return token.text.lower()

    def get_txt(token: Token) -> str:
        return token.text

    if lemmatize:
        if lowercase:
            return get_lower_lemma
        return get_lemma
    if lowercase:
        return get_lower_txt
    return get_txt


def allcap_differential_getter(span: Union[Span, Doc]) -> bool:
    """Check whether just some words in the span are ALL CAPS.

    Args:
        span (Union[Span, Doc]): A spaCy span

    Returns:
        bool: `True` if some but not all items in `words` are ALL CAPS
    """
    is_different = False
    allcap_words = 0
    for word in span:
        if word.is_upper:
            allcap_words += 1
    cap_differential = len(span) - allcap_words
    if 0 < cap_differential < len(span):
        is_different = True
    return is_different


def make_intensifier_getter(
    intensifiers: dict[str, float],
    lemmatize: bool = True,
    lowercase: bool = True,
) -> Callable[[Token], float]:
    """Creates a token getter which checks it token is an intensifier and
    return it intensification factor.

    Args:
        intensifiers (Dict[str, float]): A dictionary of intensifiers and multiplication
            factor.
        lemmatize (bool): Should it look up in the intensifiers using the lemma?
            Defaults to True.
        lowercase (bool): Should it look up in the intensifiers using the lowercased
            word? Defaults to True.

    Returns:
        Callable[[Token], float]: The getter function
    """
    t_getter = make_txt_getter(lemmatize, lowercase)

    if not Doc.has_extension("is_cap_diff"):
        Doc.set_extension("is_cap_diff", getter=allcap_differential_getter)

    def intensifier_scalar_getter(token: Token) -> float:
        """Get intensifier score for token."""
        t = t_getter(token)
        if t in intensifiers:
            scalar = intensifiers[t]
            if token.is_upper and token.doc._.is_cap_diff:
                scalar += C_INCR
            return scalar
        return 0.0

    return intensifier_scalar_getter


def make_valance_getter(
    lexicon: dict[str, float],
    lemmatize: bool = False,
    lowercase: bool = True,
    cap_differential: float = C_INCR,
) -> Callable[[Token], float]:
    """Creates a token getter which return the valence (sentiment) of a token
    including the capitalization of the token.

    Args:
        lexicon (Dict[str, float]): The valence scores of the tokens.
        lemmatize (bool): Should it look up in the lexicon (and intensifiers)
            using the lemma? Defaults to True.
        lowercase (bool): Should it look up in the lexicon (and intensifiers)
            using the lowercased word? Defaults to True.
        cap_differential (float): Capitalization differential, which is added to the
            valence of the score it is emphasized using all caps. Defaults to 0.733, an
            emperically derived constant (Hutto and Gilbert, 2014). If None it will not
            be used.

    Returns:
        Callable[[Token], float]: The getter function
    """

    t_getter = make_txt_getter(lemmatize, lowercase)

    def valence_getter(token: Token) -> float:
        t = t_getter(token)
        if (t in lexicon) and not (
            Token.has_extension("intensifier") and token._.intensifier
        ):  # if token isn't a intensifier
            return lexicon[t]
        return 0.0

    def cap_diff_valence_getter(token: Token) -> float:
        valence = valence_getter(token)
        if token.is_upper and token.sent._.is_cap_diff:
            if valence > 0:
                valence += cap_differential
            elif valence < 0:
                valence -= cap_differential
        return valence

    if cap_differential:
        if not Span.has_extension("is_cap_diff"):
            Span.set_extension(
                "is_cap_diff",
                getter=allcap_differential_getter,
                force=True,
            )
        return cap_diff_valence_getter
    return valence_getter


def make_is_negation_getter(
    negations: Iterable[str],
    lemmatize: bool = True,
    lowercase: bool = True,
) -> Callable[[Token], bool]:
    """Creates a token getter which return whether a token is a negation or
    not.

    Args:
        negations (Iterable[str]): An list of negations
        lemmatize (bool): Should it look up in negations using the lemma? Defaults to
            True.
        lowercase (bool): Should it look up in negations using the lowercased word?
            Defaults to True.

    Returns:
        Callable[[Token], bool]: A token getter
    """
    t_getter = make_txt_getter(lemmatize, lowercase)

    def is_negation(token: Token) -> bool:
        """Determine if token is negation words."""
        t = t_getter(token)
        return t in negations

    return is_negation


def make_is_contrastive_conj_getter(
    contrastive_conjugations: Iterable[str],
    lemmatize: bool = True,
    lowercase: bool = True,
) -> Callable[[Token], bool]:
    """Creates a token getter for whether a token is a constrastive
    conjugations.

    Args:
        contrastive_conjugations (Iterable[str]): A list of contrastive conjugations.
        lemmatize (bool): Should you lemmatize before lookup in the contrastive
            conjugations list? Defaults to True.
        lowercase (bool): Should you lowercase before lookup in the
            conjugations list? Defaults to True.

    Returns:
        Callable[[Token], bool]: A token getter
    """

    t_getter = make_txt_getter(lemmatize, lowercase)

    def is_contrastive_conj(token: Token) -> bool:
        """Determine if token is a contrastive conjugation."""
        t = t_getter(token)
        return t in contrastive_conjugations

    return is_contrastive_conj


def make_is_negated_getter(
    lookback: int = 3,
    is_negation_getter: Optional[Callable[[Token], bool]] = None,
) -> Callable[[Token], Optional[Token]]:
    """Creates a getter which checks if a token is negated by checked whether
    the n previous workds are negations.

    Args:
        lookback (int): How many token should it look backwards for negations? Defaults
            to 3 which is emperically derived by Hutto and Gilbert (2014).
        is_negation_getter (Optional[Callable[[Token], bool]]): A function which given a
            token return if the token is a negation or not. If None it assumes that
            the token extention "is_negation" is set. If specified overwrites the
            extension. Defualts to None.

    Returns:
        Callable[[Token], bool]: The getter function
    """
    if is_negation_getter:
        Token.set_extension("is_negation", getter=is_negation_getter, force=True)
    if not Token.has_extension("is_negation"):
        raise ValueError(
            "Token class has no extension 'is_negation', either set the extension"
            + " or provide the is_negation_getter.",
        )

    def is_negated_getter(token: Token) -> Optional[Token]:
        """Determine if token is negated."""
        # don't look back before the sentence start
        min_token_idx = max(token.sent.start, token.i - lookback)
        for t in token.doc[min_token_idx : token.i]:
            if t._.is_negation:
                return t
        return None

    return is_negated_getter


def make_token_polarity_getter(
    valence_getter: Optional[Callable[[Token], float]] = None,
    is_negated_getter: Optional[Callable[[Token], Union[bool, Optional[Token]]]] = None,
    intensifier_getter: Optional[Callable[[Token], float]] = None,
    negation_scalar: float = N_SCALAR,
    lookback_intensities: list[float] = [1.0, 0.95, 0.90],  # noqa
    **kwargs,  # noqa
) -> Callable[[Token], TokenPolarityOutput]:
    """Creates a function (getter) which takes a token and return the polarity
    of the token based upon whether the token valence (sentiment) including
    whether is negated and whether it is intensified using an intensifier.

    Args:
        valence_getter (Optional[Callable[[Token], float]]): a function which given a
            token return the valence (sentiment) of the token. If None it assumes that
            the the token extention "valence" is set. If specified it overwrites the
            extension. Defualts to None.
        is_negated_getter (Optional[Callable[[Token], bool]]): A function which given a
            token return a boolean indicating whether the token is negated. If None it
            assumes that the the token extention "is_negated" is set. If specified it
            overwrites the extension. Defualts to None.
        intensifier_getter (Optional[Callable[[Token], float]]): A getter which for a
            token return 0 if it is not an intensifier or its intensifcation value if it
            is an intensifier. E.g. the token 'especially' might have an value of 0.293
            which increases or decreases the valence of the following word by the
            specified amount. Defaults to None, intensifiers aren't included in the
            analysis of token valence.
        negation_scalar (float):  Defaults to the emperically derived constant
            -0.74 (Hutto and Gilbert, 2014).
        lookback_intensities (List[float]): How long to look back for intensifiers
            (length). Intensities indicate the how much to weight each intensifier.
            Defaults to [1.0, 0.95, 0.90] which is emperically derived
            (Hutto and Gilbert, 2014).
        **kwargs: Additional keyword arguments.

    Returns:
        Callable[[Token], TokenPolarityOutput]: The getter function
    """
    lookback = len(lookback_intensities)

    if valence_getter:
        Token.set_extension("valence", getter=valence_getter, force=True)

    if not Token.has_extension("valence"):
        raise ValueError(
            "Token class has no extension 'valence', either set the extension"
            + " or provide the valence_getter.",
        )
    if is_negated_getter:
        Token.set_extension(
            "is_negated",
            getter=is_negated_getter,
            force=True,
        )
    if not Token.has_extension("is_negated"):
        raise ValueError(
            "Token class has no extension 'is_negated', either set the extension"
            + " or provide the is_negation_getter.",
        )

    if intensifier_getter:
        Token.set_extension("intensifier", getter=intensifier_getter, force=True)
    if not Token.has_extension("intensifier"):
        Token.set_extension(
            "intensifier",
            getter=make_intensifier_getter(
                intensifiers={},
                lemmatize=False,
                lowercase=False,
            ),
        )

    def token_polarity_getter(
        token: Token,
    ) -> TokenPolarityOutput:
        valence = token._.valence

        intensifiers = []
        is_neg = None
        start_tok = token.i  # only used if span is returned
        if valence:
            for start_i in range(1, lookback + 1):
                # dampen the scalar modifier of preceding words and emoticons
                # (excluding the ones that immediately preceed the item) based
                # on their distance from the current item.

                if token.i > start_i:
                    tok_id = token.i - start_i
                    # stop if before sentence start
                    if tok_id < token.sent.start:
                        break

                    prev_token = token.doc[tok_id]
                    b = prev_token._.intensifier
                    if b != 0:
                        intensifiers.append(prev_token)
                        b = b * lookback_intensities[start_i - 1]
                        start_tok = prev_token.i
                    valence = valence + b if valence > 0 else valence - b
            is_neg = token._.is_negated
            if is_neg:
                valence = valence * negation_scalar
                if isinstance(is_neg, Token) and start_tok > is_neg.i:
                    start_tok = is_neg.i

        return TokenPolarityOutput(
            polarity=valence,
            token=token,
            span=token.doc[start_tok : token.i + 1],
            negation=is_neg,
            intensifiers=intensifiers,
        )

    return token_polarity_getter


def normalize(score: float, alpha: float = 15) -> float:
    """Normalize the score to be between -1 and 1 using an alpha that
    approximates the max expected value.

    Args:
        score: The score to normalize.
        alpha: The alpha value to use for normalization. Defaults to 15.

    Returns:
        The normalized score.
    """
    norm_score = score / math.sqrt((score * score) + alpha)
    if norm_score < -1.0:
        return -1.0
    if norm_score > 1.0:
        return 1.0
    return norm_score


def questionmark_amplification(text: str) -> float:
    """Amplified the questions."""
    # check for added emphasis resulting from question marks (2 or 3+)
    qm_count = text.count("?")
    qm_amplifier = 0.0
    if qm_count > 1:
        if qm_count <= 3:  # noqa
            # (empirically derived mean sentiment intensity rating increase for
            # question marks)
            qm_amplifier = qm_count * 0.18
        else:
            qm_amplifier = 0.96
    return qm_amplifier


def exclamation_amplification(text: str) -> float:
    # check for added emphasis resulting from exclamation points (up to 4 of them)
    ep_count = text.count("!")
    if ep_count > 4:
        ep_count = 4
    # (empirically derived mean sentiment intensity rating increase for
    # exclamation points)
    ep_amplifier = ep_count * 0.292
    return ep_amplifier


def but_check(
    span: Span,
    sentiment: list,
    before_but_scalar: float = BEFORE_BUT_SCALAR,
    after_but_scalar: float = AFTER_BUT_SCALAR,
) -> list:
    contains_but = False
    for token in span:
        if token._.is_contrastive_conj:
            but_idx = token.i
            contains_but = True
    if contains_but is not False:
        for i, s in enumerate(sentiment[0:but_idx]):  # type: ignore
            sentiment[i] = s * before_but_scalar
        for i, s in enumerate(sentiment[but_idx:]):  # type: ignore
            sentiment[i] = s * after_but_scalar
    return sentiment


def sift_sentiment_scores(sentiments: Iterable[float]) -> tuple[float, float, int]:
    """Separate positive and negative sentiment scores."""
    pos_sum = 0.0
    neg_sum = 0.0
    neu_count = 0
    for sentiment_score in sentiments:
        if sentiment_score > 0:
            pos_sum += (
                float(sentiment_score) + 1
            )  # compensates for neutral words that are counted as 1
        if sentiment_score < 0:
            neg_sum += (
                float(sentiment_score) - 1
            )  # when used with math.fabs(), compensates for neutrals
        if sentiment_score == 0:
            neu_count += 1
    return pos_sum, neg_sum, neu_count


def make_span_polarity_getter(
    polarity_getter: Optional[Callable[[Token], float]],
    contrastive_conj_getter: Optional[Callable[[Token], bool]],
) -> Callable[[Span], SpanPolarityOutput]:
    """Creates a function (getter) which for a span return the aggrated
    polarities. Including accounting for contrastive conjugations (e.g. 'but'),
    exclamationsmarks and questionmarks.

    Args:
        polarity_getter (Optional[Callable[[Token], float]]): A function which given a
            token return the polarity (sentiment) of the token. If None it assumes that
            the token extension "polarity" is already set. If given it overwrites the
            "polarity" extension. Defaults to None.
        contrastive_conj_getter (Optional[Callable[[Token], bool]]): A function which
            given a token return whether the token is a contrastive conjunction. If None
            it assumes that the token extension "is_contrastive_conj" is already set. If
            given it overwrites the "is_contrastive_conj" extension. Defaults to None.

    Returns:
        Callable[[Span], SpanPolarityOutput]: A function which for a span return the
        aggrated polarities. Including accounting for contrastive conjugations (e.g.
        'but'), exclamationsmarks and questionmarks.
    """
    if polarity_getter:
        Token.set_extension("polarity", getter=polarity_getter, force=True)
    if not Token.has_extension("polarity"):
        raise ValueError(
            "Token class has no extension 'polarity', either set the extension"
            + " or provide the polarity_getter.",
        )
    if contrastive_conj_getter:
        Token.set_extension(
            "is_contrastive_conj",
            getter=contrastive_conj_getter,
            force=True,
        )
    if not Token.has_extension("is_contrastive_conj"):
        raise ValueError(
            "Token class has no extension 'is_contrastive_conj', either set the "
            + "extension or provide the contrastive_conj_getter.",
        )

    def __extract(polarity: TokenPolarityOutput) -> tuple[float, Span]:
        return polarity.polarity, polarity.span

    def __polarity_getter(
        span: Span,
        but_check: Callable = but_check,
    ) -> SpanPolarityOutput:
        polarities = [t._.polarity for t in span]
        sentiment, spans = zip(*[__extract(p) for p in polarities])
        sentiment = but_check(span, list(sentiment))
        sum_s = float(sum(sentiment))

        if sum_s:
            # compute and add emphasis from punctuation in text
            punct_emph_amplifier = 0.0
            punct_emph_amplifier += questionmark_amplification(span.text)
            punct_emph_amplifier += exclamation_amplification(span.text)
            if sum_s > 0:
                sum_s += punct_emph_amplifier
            elif sum_s < 0:
                sum_s -= punct_emph_amplifier

            compound = normalize(sum_s)
            # discriminate between positive, negative and neutral sentiment scores
            pos_sum, neg_sum, neu_count = sift_sentiment_scores(sentiment)

            if pos_sum > math.fabs(neg_sum):
                pos_sum += punct_emph_amplifier
            elif pos_sum < math.fabs(neg_sum):
                neg_sum -= punct_emph_amplifier

            total = pos_sum + math.fabs(neg_sum) + neu_count
            pos = math.fabs(pos_sum / total)
            neg = math.fabs(neg_sum / total)
            neu = math.fabs(neu_count / total)
        else:
            compound = 0.0
            pos = 0.0
            neg = 0.0
            neu = 0.0

        return SpanPolarityOutput(
            negative=neg,
            neutral=neu,
            positive=pos,
            compound=compound,
            span=span,
            polarities=polarities,
        )

    return __polarity_getter


def make_doc_polarity_getter(
    span_polarity_getter: Optional[Callable[[Span], float]],
) -> Callable[[Doc], DocPolarityOutput]:
    """Creates a function (getter) which for a doc return the aggrated
    polarities. Including accounting for contrastive conjugations (e.g. 'but'),
    exclamationsmarks and questionmarks.

    Args:
        span_polarity_getter (Optional[Callable[[Span], float]]):  a function which
            given a span return the polarity (sentiment) of the span. If None it assumes
            that the the span extention "polarity" is already set. If specified it
            overwrites the extension. Defaults to None.

    Returns:
        Callable[[Doc], DocPolarityOutput]: A function which given a doc return the
            aggrated polarities. Including accounting for contrastive conjugations (e.g.
            'but'), exclamationsmarks and questionmarks.
    """

    if span_polarity_getter:
        Span.set_extension("polarity", getter=span_polarity_getter, force=True)
    if not Span.has_extension("polarity"):
        raise ValueError(
            "Span class has no extension 'polarity', either set the extension"
            + " or provide the span_polarity_getter.",
        )

    def polarity_getter(
        doc: Doc,
    ) -> DocPolarityOutput:
        polarities = [sent._.polarity for sent in doc.sents]
        if polarities:
            n = len(polarities)
            negative = sum(p.negative for p in polarities) / n
            positive = sum(p.positive for p in polarities) / n
            neutral = sum(p.neutral for p in polarities) / n
            compound = sum(p.compound for p in polarities) / n
        else:
            negative = 0
            positive = 0
            neutral = 0
            compound = 0

        return DocPolarityOutput(
            negative=negative,
            positive=positive,
            neutral=neutral,
            compound=compound,
            polarities=polarities,
            doc=doc,
        )

    return polarity_getter
