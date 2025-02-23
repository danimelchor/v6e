from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod
from copy import copy

from typing_extensions import override

from v6e.exceptions import ValidationException

T = t.TypeVar("T")
C = t.TypeVar("C")


class ParseResult(t.Generic[T]):
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


CheckFn = t.Callable[[T], ParseResult]


class Check(t.NamedTuple, t.Generic[T]):
    name: str
    check: CheckFn[T]


class V6eTypeType(t.Protocol[T]):
    def _chain(self: t.Self, name: str, check: CheckFn[T]) -> t.Self: ...
    def _or(self: t.Self, other: V6eType[C]) -> _Union[T, C]: ...
    def _parse(self: t.Self, raw: t.Any) -> T: ...
    def safe_parse(self: t.Self, raw: t.Any) -> ParseResult: ...
    def check(self: t.Self, raw: t.Any) -> bool: ...
    def parse(self: t.Self, raw: t.Any) -> T: ...


class V6eType(ABC, V6eTypeType[T]):
    def __init__(self) -> None:
        super().__init__()
        self._checks: list[Check[T]] = []

    def _chain(self, name: str, check: CheckFn[T]) -> t.Self:
        print(name)
        cp = copy(self)
        cp._checks.append(Check(name, check))
        return cp

    def _or(self, other: V6eType[C]) -> _Union[T, C]:
        return _Union(self, other)

    @abstractmethod
    def _parse(self, raw: t.Any) -> T: ...

    @t.final
    def safe_parse(self, raw: t.Any) -> ParseResult:
        try:
            value = self._parse(raw)
        except Exception as e:
            return ParseResult(
                error_message=f"Failed to parse {raw} as {self}",
                _cause=e,
            )

        for _, check in self._checks:
            parse_res = check(value)
            if parse_res.is_err():
                return parse_res

            # Update value for next iteration
            value = parse_res.result

        return ParseResult(result=value)

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
        checks = "".join(f".{c.name}" for c in self._checks)
        return f"{self.__class__.__name__}{checks}"


class _Union(V6eType[T | C]):
    def __init__(self, left: V6eType[T], right: V6eType[C]) -> None:
        super().__init__()
        self.left = left
        self.rigth = right

    @override
    def _parse(self, raw: t.Any) -> T | C:
        try:
            return self.left.parse(raw)
        except ValidationException:
            return self.rigth.parse(raw)
