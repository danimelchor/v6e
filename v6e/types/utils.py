from __future__ import annotations

import typing as t

from v6e.types.base import V6eTypeType


def repr_fun(fn: t.Callable[...], *args: t.Any, **kwargs: t.Any):
    repr = f"{fn.__name__}"
    if not args and not kwargs:
        return repr

    def _arg_to_str(arg: t.Any):
        if isinstance(arg, t.Callable):
            return arg.__name__
        return f"{arg!r}"

    all_args_str = "".join(
        [
            *map(_arg_to_str, args),
            *[f"{k}={_arg_to_str(v)}" for k, v in kwargs.items()],
        ]
    )
    return f"{repr}({all_args_str})"


def alias(cls: type[V6eTypeType], name: str) -> type[V6eTypeType]:
    """
    Utility to alias a V6eType with a different name
    so that they're represented differently. For example:
    ```python
    print(V6eBool().gt(5))  # v6e.V6eBool().gt(5)
    bool = alias(V6eBool, "bool")
    print(bool().gt(5))  # v6e.bool().gt(5)
    ```
    """
    return t.cast(type[V6eTypeType], type(name, (cls,), {}))
