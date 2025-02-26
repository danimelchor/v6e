import typing as t

from v6e.types.base import V6eTypeType
from v6e.types.sequences import V6eSequenceMixin


class V6eList(V6eSequenceMixin[V6eTypeType]):
    def __init__(self, inner: V6eTypeType) -> None:
        super().__init__()
        self._inner = inner

    def parse_raw(self, raw: t.Any) -> list[V6eTypeType]:
        if not isinstance(raw, list):
            raise ValueError(f"Cannot parse {raw!r} as list.")

        if len(raw) == 0:
            return raw

        list_cp = []
        for i in raw:
            value = self._inner.parse(i)
            list_cp.append(value)

        return list_cp
