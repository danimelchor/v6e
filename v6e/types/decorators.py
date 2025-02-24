from __future__ import annotations

import typing as t

from v6e.exceptions import ParseException
from v6e.types import utils
from v6e.types.result import V6eResult

if t.TYPE_CHECKING:
    from v6e.types.base import V6eTypeType

T = t.TypeVar("T")
V = t.TypeVar("V")


@t.overload
def parser(
    wrapped_fun: t.Callable[[V6eTypeType, T], T | None],
) -> t.Callable[[V6eTypeType], V6eTypeType]: ...


@t.overload
def parser(
    wrapped_fun: t.Callable[[V6eTypeType, T, V], T | None],
) -> t.Callable[[V6eTypeType, V], V6eTypeType]: ...


def parser(
    wrapped_fun: t.Callable[[V6eTypeType, T], T | None]
    | t.Callable[[V6eTypeType, T, V], T | None],
) -> t.Callable[[V6eTypeType], V6eTypeType] | t.Callable[[V6eTypeType, V], V6eTypeType]:
    """
    Converts a function taking a value and any arbitrary arguments into a
    chainable parser function. The function must take in the value being parsed as
    the first argument, and any other args will be specified by the user. Additionally,
    the function must return a value of the same type as the one being passed by the user
    or None to return the same.
    """

    def _impl(self: V6eTypeType, *args, **kwargs) -> V6eTypeType:
        # Create the function we will chain
        def _fn(value: T) -> V6eResult[T]:
            try:
                res = wrapped_fun(self, value, *args, **kwargs)
            except (ValueError, TypeError, ParseException) as e:
                err_msg = t.cast(str, kwargs.get("msg", str(e)))
                return V6eResult(error_message=err_msg.format(value))

            return V6eResult(
                result=value if res is None else res,
            )

        # Get a string representation
        repr = utils.repr_fun(wrapped_fun, *args, **kwargs)

        # Chain it
        return self.chain(repr, _fn)

    return _impl
