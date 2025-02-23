from __future__ import annotations

import typing as t

from v6e.exceptions import ValidationException
from v6e.types.base import ParseResult, V6eTypeType

T = t.TypeVar("T", bound=V6eTypeType)
X = t.TypeVar("X")
V = t.TypeVar("V")
P = t.ParamSpec("P")


def parser(wrapped_fun: t.Callable[t.Concatenate[T, V, P], None]):
    def _impl(self: T, *args: P.args, **kwargs: P.kwargs) -> T:
        repr = f"{wrapped_fun.__name__}"

        def _fn(value: V):
            try:
                res = wrapped_fun(self, value, *args, **kwargs)
            except (ValueError, TypeError, ValidationException) as e:
                return ParseResult(error_message=str(e))

            return ParseResult(
                result=value if res is None else res,
            )

        self._chain(repr, _fn)
        return self

    return _impl
