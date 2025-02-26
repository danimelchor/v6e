from __future__ import annotations

import typing as t

from v6e.types.base import V6eType, parser

T = t.TypeVar("T", bound=t.Sequence)


class V6eSequenceMixin(V6eType[T]):
    @parser
    def length(self, value: T, x: int, /, msg: str | None = None):
        if len(value) != x:
            raise ValueError(
                f"The length of {value} is not {x} (it's {len(value)})",
            )

    @parser
    def contains(self, value: T, x: T, /, msg: str | None = None):
        if x not in value:
            raise ValueError(
                f"{value} does not contain {x}",
            )
