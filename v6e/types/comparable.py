from __future__ import annotations

import typing as t

from v6e.types.base import V6eType


class _Comparable(t.Protocol):
    def __lt__(self, other: t.Self, /) -> bool: ...
    def __gt__(self, other: t.Self, /) -> bool: ...
    def __le__(self, other: t.Self, /) -> bool: ...
    def __ge__(self, other: t.Self, /) -> bool: ...


Comparable = t.TypeVar("Comparable", bound=_Comparable)


class V6eComparableMixin(V6eType[Comparable]):
    def gt(self, value: Comparable) -> t.Self:
        return self._chain(
            f"gt({value})",
            lambda x: x > value,
            f"Value {{}} must be greater than {value}",
        )

    def gte(self, value: Comparable, *, _name: str = "gte") -> t.Self:
        return self._chain(
            f"{_name}({value})",
            lambda x: x >= value,
            f"Value {{}} must be greater than or equal to {value}",
        )

    def lt(self, value: Comparable) -> t.Self:
        return self._chain(
            f"lt({value})",
            lambda x: x < value,
            f"Value {{}} must less than {value}",
        )

    def lte(self, value: Comparable, *, _name: str = "lte") -> t.Self:
        return self._chain(
            f"{_name}({value})",
            lambda x: x <= value,
            f"Value {{}} must less than or equal to {value}",
        )

    def min(self, value: Comparable) -> t.Self:
        return self.gte(value, _name="min")

    def max(self, value: Comparable) -> t.Self:
        return self.lte(value, _name="max")
