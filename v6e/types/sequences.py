from __future__ import annotations

import typing as t

from v6e.types.base import V6eType, parser

T = t.TypeVar("T")


class V6eSequenceMixin(V6eType[t.Sequence[T]]):
    @parser
    def length(self, value: t.Sequence[T], x: int, /, msg: str | None = None):
        if len(value) != x:
            raise ValueError(
                f"The length of {value} is not {x} (it's {len(value)})",
            )

    @parser
    def max(self, value: t.Sequence[T], x: int, /, msg: str | None = None):
        if len(value) > x:
            raise ValueError(
                f"The length of {value} has to be at most {x} (it's {len(value)})",
            )

    @parser
    def min(self, value: t.Sequence[T], x: int, /, msg: str | None = None):
        if len(value) < x:
            raise ValueError(
                f"The length of {value} has to be at least {x} (it's {len(value)})",
            )

    @parser
    def contains(self, value: t.Sequence[T], x: T, /, msg: str | None = None):
        if x not in value:
            raise ValueError(
                f"{value} does not contain {x}",
            )

    @parser
    def nonempty(self, value: t.Sequence[T], /, msg: str | None = None):
        if len(value) == 0:
            raise ValueError(f"The value {value} is empty")
