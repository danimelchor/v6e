import typing as t

from v6e.types.base import V6eType


class V6eDict(V6eType[dict[str, t.Any]]):
    def __init__(self, **definition: V6eType[t.Any]) -> None:
        self.definition = definition
        super().__init__()

    def parse_raw(self, raw: t.Any) -> dict[str, t.Any]:
        if not isinstance(raw, dict):
            raise ValueError(f"Value {raw!r} cannot be parsed as a dictionary")

        cp_raw = {}
        for field in self.definition:
            if field not in raw:
                raise ValueError(
                    f"Dict {raw!r} does not contain required field {field!r}"
                )

            value = raw[field]
            field_parser = self.definition[field]
            cp_raw[field] = field_parser.parse(value)

        return cp_raw

    def repr_args(self) -> str:
        args_str = [f"{k}={v}" for k, v in self.definition.items()]
        return ", ".join(args_str)
