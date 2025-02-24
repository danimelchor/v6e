from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod
from copy import copy

from typing_extensions import override

from v6e.exceptions import ParseException
from v6e.types.decorators import parser
from v6e.types.result import V6eResult

T = t.TypeVar("T")
C = t.TypeVar("C")
P = t.ParamSpec("P")
R = t.TypeVar("R")
V6eTypeType = t.TypeVar("V6eTypeType", bound="V6eType")


class CheckFn(t.Protocol[T]):
    def __call__(self, value: T) -> V6eResult[T]: ...


class Check(t.NamedTuple, t.Generic[T]):
    name: str
    check: CheckFn[T]


class V6eType(ABC, t.Generic[T]):
    def __init__(self, _alias: str | None = None) -> None:
        super().__init__()
        self._checks: list[Check[T]] = []
        self._alias: str | None = _alias

    @abstractmethod
    def parse_raw(self, raw: t.Any) -> T: ...

    def chain(self, name: str, check: CheckFn[T]) -> t.Self:
        cp = copy(self)
        cp._checks.append(Check(name, check))
        return cp

    def __or__(self, other: V6eType[C]) -> V6eUnion[T, C]:
        return V6eUnion(self, other)

    @t.final
    def safe_parse(self, raw: t.Any) -> V6eResult[T]:
        try:
            value = self.parse_raw(raw)
        except (ValueError, TypeError, ParseException) as e:
            return V6eResult(
                error_message=f"Failed to parse {raw} as {self}",
                _cause=e,
            )

        for _, check in self._checks:
            parse_res = check(value)
            if parse_res.is_err():
                return parse_res

            # Update value for next iteration
            value = parse_res.result

        return V6eResult(result=value)

    @t.final
    def check(self, raw: t.Any) -> bool:
        return self.safe_parse(raw).is_ok()

    @t.final
    def parse(self, raw: t.Any) -> T:
        parse_res = self.safe_parse(raw)
        if parse_res.is_err():
            raise parse_res.get_exception()
        return parse_res.result

    @t.final
    def __call__(self, raw: t.Any) -> T:
        return self.parse(raw)

    @parser
    def custom(self, value: T, fn: t.Callable[[T], T | None]) -> T | None:
        return fn(value)

    def repr_args(self) -> str:
        return ""

    @override
    def __repr__(self):
        name = self._alias or self.__class__.__name__
        checks = "".join(f".{c.name}" for c in self._checks)
        return f"v6e.{name}({self.repr_args()}){checks}"


class V6eUnion(V6eType[T | C]):
    def __init__(self, left: V6eType[T], right: V6eType[C]) -> None:
        super().__init__()
        self.left = left
        self.right = right

    @override
    def parse_raw(self, raw: t.Any) -> T | C:
        try:
            return self.left.parse(raw)
        except ParseException:
            return self.right.parse(raw)

    @override
    def __repr__(self):
        return f"{self.left} | {self.right}"
