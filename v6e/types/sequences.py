from __future__ import annotations

import typing as t

from v6e.types.base import V6eType, parser

T = t.TypeVar("T", bound=t.Sequence)


class V6eSequenceMixin(V6eType[T]):
    @parser
    def length(self, value: T, x: int):
        if len(value) != x:
            raise ValueError(
                f"The length of {value} was not {x}",
            )

    @parser
    def contains(self, value: T, x: T):
        if x not in value:
            raise ValueError(
                f"{value} does not contain {x}",
            )
