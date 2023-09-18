from typing import Any, Union

from pydantic import BaseModel
from spacy.tokens import Doc, Span, Token


class TokenPolarityOutput(BaseModel):
    """A data class for the polarity output of a span, notably allows for
    plotting the output."""

    class Config:
        arbitrary_types_allowed = True

    polarity: float
    token: Token
    span: Span
    negation: Union[Token, None] = None
    intensifiers: list[Token] = []

    def __repr_str__(self, join_str: str) -> str:
        return join_str.join(
            repr(v) if a is None else f"{a}={v!r}"
            for a, v in [
                ("polarity", round(self.polarity, 3)),
                ("token", self.token),
                ("span", self.span),
            ]
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, (TokenPolarityOutput, float)):
            return NotImplemented
        if isinstance(other, TokenPolarityOutput):
            other = other.polarity
        return self.polarity < other

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (TokenPolarityOutput, float)):
            return NotImplemented
        if isinstance(other, TokenPolarityOutput):
            other = other.polarity
        return self.polarity == other

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, (TokenPolarityOutput, float)):
            return NotImplemented
        if isinstance(other, TokenPolarityOutput):
            other = other.polarity
        return self.polarity > other

    def __bool__(self) -> bool:
        return bool(self.polarity)

    def to_dict(self) -> dict[str, Any]:
        span_range = self.span.start, self.span.end
        negation_index = self.negation.i if self.negation else None
        intensifier_indices = [t.i for t in self.intensifiers]
        token_index = self.token.i

        return {
            "polarity": self.polarity,
            "token": token_index,
            "span_index": span_range,
            "negation_index": negation_index,
            "intensifier_indices": intensifier_indices,
        }

    @classmethod
    def from_dict(
        cls: type["TokenPolarityOutput"],
        obj: dict[str, Any],
        doc: Doc,
    ) -> "TokenPolarityOutput":
        span = doc[obj["span_index"][0] : obj["span_index"][1] + 1]
        negation = doc[obj["negation_index"]] if obj["negation_index"] else None
        intensifiers = [doc[i] for i in obj["intensifier_indices"]]
        token = doc[obj["token"]]

        return TokenPolarityOutput(
            polarity=obj["polarity"],
            token=token,
            span=span,
            negation=negation,
            intensifiers=intensifiers,
        )


class SpanPolarityOutput(BaseModel):
    """A data class for the polarity output of a span, notably allows for
    plotting the output."""

    class Config:
        arbitrary_types_allowed = True

    negative: float
    neutral: float
    positive: float
    compound: float
    span: Span
    polarities: list[TokenPolarityOutput]

    def __repr_str__(self, join_str: str) -> str:
        return join_str.join(
            repr(v) if a is None else f"{a}={v!r}"
            for a, v in [
                ("neg", round(self.negative, 3)),
                ("neu", round(self.neutral, 3)),
                ("pos", round(self.positive, 3)),
                ("compound", round(self.compound, 4)),
                ("span", self.span),
            ]
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, (SpanPolarityOutput, float)):
            return NotImplemented
        if isinstance(other, SpanPolarityOutput):
            other = other.compound
        return self.compound < other

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (SpanPolarityOutput, float)):
            return NotImplemented
        if isinstance(other, SpanPolarityOutput):
            other = other.compound
        return self.compound == other

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, (SpanPolarityOutput, float)):
            return NotImplemented
        if isinstance(other, SpanPolarityOutput):
            other = other.compound
        return self.compound > other

    def to_dict(self) -> dict[str, Any]:
        span_index = self.span.start, self.span.end
        return {
            "negative": self.negative,
            "neutral": self.neutral,
            "positive": self.positive,
            "compound": self.compound,
            "span_index": span_index,
            "polarities": [pol.to_dict() for pol in self.polarities],
        }

    @classmethod
    def from_dict(
        cls: type["SpanPolarityOutput"],
        obj: dict[str, Any],
        doc: Doc,
    ) -> "SpanPolarityOutput":
        span = doc[obj["span_index"][0] : obj["span_index"][1]]
        return SpanPolarityOutput(
            negative=obj["negative"],
            neutral=obj["neutral"],
            positive=obj["positive"],
            compound=obj["compound"],
            span=span,
            polarities=[
                TokenPolarityOutput.from_dict(pol, doc) for pol in obj["polarities"]
            ],
        )


class DocPolarityOutput(BaseModel):
    """A data class for the polarity output of a doc."""

    class Config:
        arbitrary_types_allowed = True

    negative: float
    neutral: float
    positive: float
    compound: float
    doc: Doc
    polarities: list[SpanPolarityOutput]

    def __repr_str__(self, join_str: str) -> str:
        return join_str.join(
            repr(v) if a is None else f"{a}={v!r}"
            for a, v in [
                ("neg", round(self.negative, 3)),
                ("neu", round(self.neutral, 3)),
                ("pos", round(self.positive, 3)),
                ("compound", round(self.compound, 4)),
            ]
        )

    def as_span_polarity(self) -> SpanPolarityOutput:
        span = self.doc.doc[:]
        pol = SpanPolarityOutput(
            negative=self.negative,
            positive=self.positive,
            neutral=self.neutral,
            compound=self.compound,
            span=span,
            polarities=[
                t_pol for span_pol in self.polarities for t_pol in span_pol.polarities
            ],
        )
        return pol

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, (DocPolarityOutput, float)):
            return NotImplemented
        if isinstance(other, DocPolarityOutput):
            other = other.compound
        return self.compound < other

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (DocPolarityOutput, float)):
            return NotImplemented
        if isinstance(other, DocPolarityOutput):
            other = other.compound
        return self.compound == other

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, (DocPolarityOutput, float)):
            return NotImplemented
        if isinstance(other, DocPolarityOutput):
            other = other.compound
        return self.compound > other

    def to_dict(self) -> dict[str, Any]:
        return {
            "negative": self.negative,
            "neutral": self.neutral,
            "positive": self.positive,
            "compound": self.compound,
            "polarities": [pol.to_dict() for pol in self.polarities],
        }

    @classmethod
    def from_dict(
        cls: type["DocPolarityOutput"],
        obj: dict[str, Any],
        doc: Doc,
    ) -> "DocPolarityOutput":
        return DocPolarityOutput(
            negative=obj["negative"],
            neutral=obj["neutral"],
            positive=obj["positive"],
            compound=obj["compound"],
            doc=doc,
            polarities=[
                SpanPolarityOutput.from_dict(pol, doc) for pol in obj["polarities"]
            ],
        )
