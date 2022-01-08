from typing import Callable, Optional

from spacy.tokens import Token
from functools import partial

def is_negation(token: Token) -> bool:
    """checks is token is a negation

    Args:
        token (Token): A spaCy token

    Returns:
        bool: a boolean indicating whether the token is a negation
    """
    m_dict = token.morph.to_dict()
    return (
        "Polarity" in m_dict  # if is has the polarity attribute
        and m_dict["Polarity"] == "Neg"
    )  # and it is negative


def is_negated(token: Token, is_negation_getter: Callable) -> Optional[Token]:
    """checks is token is negated

    Args:
        token (Token): A spaCy token

    Returns:
        Optional[Token]: return the negation if the token is negated
    """
    # only check if a word is negated if it is rated (it is not meaningful to do otherwise)
    if token._.valence:
        for c in token.children:
            # if the token is modified by a negation
            if c.dep_ == "advmod" and is_negation_getter(c):
                return c
        # or if its head it negated:
        for c in token.head.children:
            if c.dep_ == "advmod" and is_negation_getter(c):
                return c



def is_negated(token: Token, is_negation_getter: Callable) -> Optional[Token]:
    """checks is token is negated

    Args:
        token (Token): A spaCy token

    Returns:
        Optional[Token]: return the negation if the token is negated
    """
    # only check if a word is negated if it is rated (it is not meaningful to do otherwise)
    if token._.valence:
        for c in token.children:
            # if the token is modified by a negation
            if c.dep_ == "advmod" and is_negation_getter(c):
                return c
        # or if its head it negated:
        for c in token.head.children:
            if c.dep_ == "advmod" and is_negation_getter(c):
                return c
