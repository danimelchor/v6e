from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod
from copy import copy
from datetime import datetime, timedelta

from typing_extensions import override


class ValidationException(Exception):
    pass


T = t.TypeVar("T")
O = t.TypeVar("O")

V6eCheckFn = t.Callable[[T], str | None]


class V6eCheck(t.Generic[T]):
    __slots__ = ("_fn", "_name")

    def __init__(self, name: str, fn: V6eCheckFn[T]) -> None:
        self._fn = fn
        self._name = name

    def __call__(self, x: T) -> str | None:
        return self._fn(x)

    def __repr__(self):
        return f".{self._name}"


class V6eType(ABC, t.Generic[T]):
    def __init__(self) -> None:
        super().__init__()
        self._checks: list[V6eCheck] = []

    def _chain(self, name: str, check: V6eCheckFn[T]) -> t.Self:
        cp = copy(self)
        cp._checks.append(V6eCheck(name, check))
        return cp

    def _or(self, other: V6eType[O]) -> _V6eUnion[T, O]:
        return _V6eUnion(self, other)

    def _fn(self, fn: t.Callable[[T], bool], err: str) -> V6eCheckFn[T]:
        def inner(x: T) -> None:
            if not fn(x):
                raise ValidationException(err.format(x))

        return inner

    @abstractmethod
    def parse(self, raw: t.Any) -> T: ...

    @t.final
    def check(self, raw: t.Any) -> None:
        value = self.parse(raw)
        for check in self._checks:
            err = check(value)
            if err is not None:
                raise ValidationException(err)

    @override
    def __repr__(self):
        checks = "".join(map(str, self._checks))
        return f"{self.__class__.__name__}{checks}"


class _V6eUnion(V6eType[T | O]):
    def __init__(self, left: V6eType[T], right: V6eType[O]) -> None:
        super().__init__()
        self.left = left
        self.rigth = right

    @override
    def parse(self, raw: t.Any) -> T | O:
        try:
            return self.left.parse(raw)
        except ValidationException:
            return self.rigth.parse(raw)


Numeric: t.TypeAlias = int | float


class V6eIntType(V6eType[int]):
    @override
    def parse(self, raw):
        return int(raw)

    def min(self, value: Numeric) -> t.Self:
        return self._chain(
            f"min({value})",
            self._fn(lambda x: x >= value, f"Value {{}} must be at least {value}"),
        )

    def max(self, value: Numeric) -> t.Self:
        return self._chain(
            f"max({value})",
            self._fn(lambda x: x <= value, f"Value {{}} must be at most {value}"),
        )

    def positive(self) -> t.Self:
        return self._chain(
            "positive()", self._fn(lambda x: x > 0, "Value {} must be positive")
        )

    def negative(self) -> t.Self:
        return self._chain(
            "negative()", self._fn(lambda x: x < 0, "Value {} must be negative")
        )


class V6eFloatType(V6eType[float]):
    pass


class V6eStrType(V6eType[str]):
    pass


class V6eBoolType(V6eType[bool]):
    pass


class V6eDateTimeType(V6eType[datetime]):
    pass


class V6eTimeDeltaType(V6eType[timedelta]):
    pass
