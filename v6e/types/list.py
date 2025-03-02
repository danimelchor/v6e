import typing as t

from v6e.types.base import V6eType, parser

T = t.TypeVar("T")


class V6eList(V6eType[list[T]]):
    def __init__(self, inner: V6eType[T]) -> None:
        super().__init__()
        self._inner = inner

    def parse_raw(self, raw: t.Any) -> list[T]:
        if not isinstance(raw, list):
            raise ValueError(f"Cannot parse {raw!r} as list.")

        if len(raw) == 0:
            return raw

        list_cp = []
        for i in raw:
            value = self._inner.parse(i)
            list_cp.append(value)

        return list_cp

    @parser
    def length(self, value: list[T], x: int, /, msg: str | None = None):
        if len(value) != x:
            raise ValueError(
                f"The length of {value} is not {x} (it's {len(value)})",
            )

    @parser
    def max(self, value: list[T], x: int, /, msg: str | None = None):
        if len(value) > x:
            raise ValueError(
                f"The length of {value} has to be at most {x} (it's {len(value)})",
            )

    @parser
    def min(self, value: list[T], x: int, /, msg: str | None = None):
        if len(value) < x:
            raise ValueError(
                f"The length of {value} has to be at least {x} (it's {len(value)})",
            )

    @parser
    def contains(self, value: list[T], x: T, /, msg: str | None = None):
        if x not in value:
            raise ValueError(
                f"{value} does not contain {x}",
            )

    @parser
    def nonempty(self, value: list[T], /, msg: str | None = None):
        if len(value) == 0:
            raise ValueError(f"The value {value} is empty")

    def repr_args(self) -> str:
        return str(self._inner)
