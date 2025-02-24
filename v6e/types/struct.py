import typing as t
from copy import copy

from v6e.types.base import V6eType


class V6eStruct(V6eType[t.Any]):
    def __init__(self, **definition: V6eType[t.Any]) -> None:
        super().__init__()
        self.definition = definition

    def parse_raw(self, raw: t.Any) -> t.Any:
        raw_cp = copy(raw)

        for field in self.definition:
            value = getattr(raw, field, None)
            if value is None:
                raise ValueError(f"Object {raw!r} does not contain field {field!r}")

            field_parser = self.definition[field]
            setattr(raw_cp, field, field_parser.parse(value))

        return raw_cp

    def repr_args(self) -> str:
        args_str = [f"{k}={v}" for k, v in self.definition.items()]
        return ", ".join(args_str)
