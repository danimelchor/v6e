from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod
from copy import copy

from typing_extensions import override

from v6e.exceptions import ValidationException

T = t.TypeVar("T")
O = t.TypeVar("O")

V6eCheckFn = t.Callable[[T], bool]


class V6eCheck(t.Generic[T]):
    __slots__ = ("_fn", "_name", "_error_message")

    def __init__(self, name: str, fn: V6eCheckFn[T], error_message: str) -> None:
        self._fn = fn
        self._name = name
        self._error_message = error_message

    def __call__(self, x: T) -> str | None:
        if not self._fn(x):
            return self._error_message.format(x)
        return None

    def __repr__(self):
        return f".{self._name}"


class V6eType(ABC, t.Generic[T]):
    def __init__(self) -> None:
        super().__init__()
        self._checks: list[V6eCheck] = []

    def _chain(self, name: str, check: V6eCheckFn[T], error_message: str) -> t.Self:
        cp = copy(self)
        cp._checks.append(V6eCheck(name, check, error_message))
        return cp

    def _or(self, other: V6eType[O]) -> _V6eUnion[T, O]:
        return _V6eUnion(self, other)

    @abstractmethod
    def _parse(self, raw: t.Any) -> T: ...

    @t.final
    def check(self, raw: t.Any) -> bool:
        value = self._parse(raw)
        for check in self._checks:
            err = check(value)
            if err is not None:
                return False
        return True

    @t.final
    def parse(self, raw: t.Any) -> T:
        value = self._parse(raw)
        for check in self._checks:
            err = check(value)
            if err is not None:
                raise ValidationException(err)
        return value

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
    def _parse(self, raw: t.Any) -> T | O:
        try:
            return self.left.parse(raw)
        except ValidationException:
            return self.rigth.parse(raw)
