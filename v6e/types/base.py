from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod
from copy import copy

from typing_extensions import override

from v6e.exceptions import ValidationException

T = t.TypeVar("T")
P = t.TypeVar("P")

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


class V6eParseResult(t.Generic[T]):
    __slots__ = ("_result", "_error_message", "_cause")

    def __init__(
        self,
        result: T | None = None,
        error_message: str | None = None,
        _cause: Exception | None = None,
    ) -> None:
        self._result = result
        self._error_message = error_message
        self._cause = _cause

    def is_err(self) -> bool:
        return self._error_message is not None

    def is_ok(self) -> bool:
        return self._error_message is None

    @property
    def result(self) -> T:
        assert self._result is not None
        return self._result

    def get_exception(self) -> ValidationException:
        assert self._error_message is not None
        exc = ValidationException(self._error_message)
        if self._cause:
            exc.__cause__ = self._cause
        return exc


class V6eType(ABC, t.Generic[T]):
    def __init__(self) -> None:
        super().__init__()
        self._checks: list[V6eCheck] = []

    def _chain(self, name: str, check: V6eCheckFn[T], error_message: str) -> t.Self:
        cp = copy(self)
        cp._checks.append(V6eCheck(name, check, error_message))
        return cp

    def _or(self, other: V6eType[P]) -> _V6eUnion[T, P]:
        return _V6eUnion(self, other)

    @abstractmethod
    def _parse(self, raw: t.Any) -> T: ...

    @t.final
    def safe_parse(self, raw: t.Any) -> V6eParseResult:
        try:
            value = self._parse(raw)
        except Exception as e:
            return V6eParseResult(
                error_message=f"Failed to parse {raw} as {self}",
                _cause=e,
            )

        for check in self._checks:
            if err := check(value):
                return V6eParseResult(error_message=err)
        return V6eParseResult(result=value)

    @t.final
    def check(self, raw: t.Any) -> bool:
        return self.safe_parse(raw).is_ok()

    @t.final
    def parse(self, raw: t.Any) -> T:
        parse_res = self.safe_parse(raw)
        if parse_res.is_err():
            raise parse_res.get_exception()
        return parse_res.result

    @override
    def __repr__(self):
        checks = "".join(map(str, self._checks))
        return f"{self.__class__.__name__}{checks}"


class _V6eUnion(V6eType[T | P]):
    def __init__(self, left: V6eType[T], right: V6eType[P]) -> None:
        super().__init__()
        self.left = left
        self.rigth = right

    @override
    def _parse(self, raw: t.Any) -> T | P:
        try:
            return self.left.parse(raw)
        except ValidationException:
            return self.rigth.parse(raw)
