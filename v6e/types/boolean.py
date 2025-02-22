import typing as t

from typing_extensions import override

from v6e.types.base import V6eType


class V6eBoolType(V6eType[bool]):
    @override
    def _parse(self, raw):
        return bool(raw)

    def is_true(self) -> t.Self:
        return self._chain(
            "is_true()",
            lambda x: x,
            "Value {} must be greater true",
        )

    def is_false(self) -> t.Self:
        return self._chain(
            "is_false()",
            lambda x: not x,
            "Value {} must be greater true",
        )
