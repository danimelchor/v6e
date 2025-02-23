from __future__ import annotations

import typing as t

from v6e.exceptions import ValidationException
from v6e.types.base import ParseResult, V6eType

V = t.TypeVar("V")
T = t.TypeVar("T", bound=V6eType)
P = t.ParamSpec("P")

ParserFn: t.TypeAlias = t.Callable[t.Concatenate[T, V, P], V | None]


def _repr_fun(wrapped_fun: ParserFn[T, V, P], *args: P.args, **kwargs: P.kwargs):
    repr = f"{wrapped_fun.__name__}"
    if not args and not kwargs:
        return repr

    all_args_str = "".join(
        [
            *[str(a) for a in args],
            *[f"{k}={v}" for k, v in kwargs.items()],
        ]
    )
    return f"{repr}({all_args_str})"


def parser(wrapped_fun: ParserFn[T, V, P]):
    def _impl(self: T, *args: P.args, **kwargs: P.kwargs) -> T:
        repr = _repr_fun(wrapped_fun, *args, **kwargs)

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
