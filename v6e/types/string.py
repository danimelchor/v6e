from typing_extensions import override

from v6e.types.comparable import V6eComparableMixin


class V6eStrType(V6eComparableMixin[str]):
    @override
    def _parse(self, raw):
        if not isinstance(raw, str):
            raise ValueError(f"The value {raw!r} is not a valid string.")
        return raw
