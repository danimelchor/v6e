from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod
from copy import copy

from typing_extensions import override

from v6e.exceptions import ValidationException
from v6e.types import utils

T = t.TypeVar("T")
C = t.TypeVar("C")
P = t.ParamSpec("P")
V6eTypeType = t.TypeVar("V6eTypeType", bound="V6eType")


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


CheckFn: t.TypeAlias = t.Callable[[T], ParseResult]


class Check(t.NamedTuple, t.Generic[T]):
    name: str
    check: CheckFn[T]


ParserFn: t.TypeAlias = t.Callable[t.Concatenate[V6eTypeType, T, P], T | None]


def parser(wrapped_fun: ParserFn[V6eTypeType, T, P]):
    def _impl(self: V6eTypeType, *args: P.args, **kwargs: P.kwargs) -> V6eTypeType:
        def _fn(value: T):
            try:
                res = wrapped_fun(self, value, *args, **kwargs)
            except (ValueError, TypeError, ValidationException) as e:
                return ParseResult(error_message=str(e))

            return ParseResult(
                result=value if res is None else res,
            )

        repr = utils.repr_fun(wrapped_fun, *args, **kwargs)
        self._chain(repr, _fn)
        return self

    return _impl


class V6eType(ABC, t.Generic[T]):
    def __init__(self, alias: str | None = None) -> None:
        super().__init__()
        self._checks: list[Check[T]] = []
        self._alias = alias

    @abstractmethod
    def parse_raw(self, raw: t.Any) -> T: ...

    def _chain(self, name: str, check: CheckFn[T]) -> t.Self:
        cp = copy(self)
        cp._checks.append(Check(name, check))
        return cp

    def _or(self, other: V6eType[C]) -> _Union[T, C]:
        return _Union(self, other)

    @t.final
    def safe_parse(self, raw: t.Any) -> ParseResult[T]:
        try:
            value = self.parse_raw(raw)
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

    @parser
    def custom(self, value: T, fn: t.Callable[[T], T | None]) -> T | None:
        return fn(value)

    @override
    def __repr__(self):
        name = self._alias or self.__class__.__name__
        checks = "".join(f".{c.name}" for c in self._checks)
        return f"v6e.{name}(){checks}"


class _Union(V6eType[T | C]):
    def __init__(self, left: V6eType[T], right: V6eType[C]) -> None:
        super().__init__()
        self.left = left
        self.rigth = right

    @override
    def parse_raw(self, raw: t.Any) -> T | C:
        try:
            return self.left.parse(raw)
        except ValidationException:
            return self.rigth.parse(raw)
