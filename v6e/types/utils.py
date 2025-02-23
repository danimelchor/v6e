from __future__ import annotations

import typing as t

from v6e.types.base import ParserFn, V6eTypeType

P = t.ParamSpec("P")
T = t.TypeVar("T")


def repr_fun(fn: ParserFn[V6eTypeType, T, P], *args: P.args, **kwargs: P.kwargs):
    repr = f"{fn.__name__}"
    if not args and not kwargs:
        return repr

    all_args_str = "".join(
        [
            *[f"{a!r}" for a in args],
            *[f"{k}={v!r}" for k, v in kwargs.items()],
        ]
    )
    return f"{repr}({all_args_str})"


def alias(cls: type[V6eTypeType], name: str) -> t.Callable[[], V6eTypeType]:
    """
    Utility to alias a V6eType with a different name
    so that they're represented differently. For example:
    ```python
    print(V6eBool().gt(5))  # v6e.V6eBool().gt(5)
    bool = alias(V6eBool, "bool")
    print(bool().gt(5))  # v6e.bool().gt(5)
    ```
    """

    def inner():
        return cls(alias=name)

    return inner
