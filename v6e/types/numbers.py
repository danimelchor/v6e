from __future__ import annotations

import typing as t

from typing_extensions import override

from v6e.types.base import V6eType

Numeric = t.TypeVar("Numeric", bound=int | float)


class NumericMixin(V6eType[Numeric]):
    def gt(self, value: Numeric) -> t.Self:
        return self._chain(
            f"gt({value})",
            lambda x: x > value,
            f"Value {{}} must be greater than {value}",
        )

    def gte(self, value: Numeric, *, _name: str = "gte") -> t.Self:
        return self._chain(
            f"{_name}({value})",
            lambda x: x >= value,
            f"Value {{}} must be greater than or equal to {value}",
        )

    def lt(self, value: Numeric) -> t.Self:
        return self._chain(
            f"lt({value})",
            lambda x: x < value,
            f"Value {{}} must less than {value}",
        )

    def lte(self, value: Numeric, *, _name: str = "lte") -> t.Self:
        return self._chain(
            f"{_name}({value})",
            lambda x: x <= value,
            f"Value {{}} must less than or equal to {value}",
        )

    def min(self, value: Numeric) -> t.Self:
        return self.gte(value, _name="min")

    def max(self, value: Numeric) -> t.Self:
        return self.lte(value, _name="max")

    def positive(self) -> t.Self:
        return self._chain("positive()", lambda x: x > 0, "Value {} must be positive")

    def nonpositive(self) -> t.Self:
        return self._chain(
            "nonpositive()", lambda x: x <= 0, "Value {} must not be positive"
        )

    def negative(self) -> t.Self:
        return self._chain("negative()", lambda x: x < 0, "Value {} must be negative")

    def nonnegative(self) -> t.Self:
        return self._chain(
            "nonnegative()", lambda x: x >= 0, "Value {} must not be negative"
        )

    def multiple_of(self, value: Numeric, *, _name="multiple_of") -> t.Self:
        return self._chain(
            f"{_name}({value})",
            lambda x: x % value == 0,
            f"Value {{}} must be a multiple of {value}",
        )

    def step(self, value: Numeric) -> t.Self:
        return self.multiple_of(value, _name="step")


class V6eIntType(NumericMixin[int]):
    @override
    def _parse(self, raw):
        value = int(raw)
        if value != float(raw):
            raise ValueError(f"The value {raw!r} is not a valid integer.")
        return value


class V6eFloatType(NumericMixin[float]):
    @override
    def _parse(self, raw):
        return float(raw)
