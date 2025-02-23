from __future__ import annotations

import typing as t

from v6e.types.base import V6eType
from v6e.types.utils import parser


class _Comparable(t.Protocol):
    def __lt__(self, other: t.Self, /) -> bool: ...
    def __gt__(self, other: t.Self, /) -> bool: ...
    def __le__(self, other: t.Self, /) -> bool: ...
    def __ge__(self, other: t.Self, /) -> bool: ...


Comparable = t.TypeVar("Comparable", bound=_Comparable)


class ComparableMixin(V6eType[Comparable]):
    @parser
    def gt(self, value: Comparable, x: Comparable):
        if value <= x:
            raise ValueError(
                f"Value {x} must be greater than {value}",
            )

    @parser
    def gte(self, value: Comparable, x: Comparable):
        if value < x:
            raise ValueError(
                f"Value {x} must be greater than or equal to {value}",
            )

    @parser
    def lt(self, value: Comparable, x: Comparable):
        if value >= x:
            raise ValueError(
                f"Value {x} must less than {value}",
            )

    @parser
    def lte(self, value: Comparable, x: Comparable):
        if value > x:
            raise ValueError(
                f"Value {x} must less than or equal to {value}",
            )

    @parser
    def min(self, value: Comparable, x: Comparable):
        if value < x:
            raise ValueError(
                f"Value {x} must be greater than or equal to {value}",
            )

    @parser
    def max(self, value: Comparable, x: Comparable):
        if value > x:
            raise ValueError(
                f"Value {x} must less than or equal to {value}",
            )
