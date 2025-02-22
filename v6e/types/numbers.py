from __future__ import annotations

import typing as t

from typing_extensions import override

from v6e.types.comparable import ComparableMixin

Numeric = t.TypeVar("Numeric", bound=int | float)


class NumericMixin(ComparableMixin[Numeric]):
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


class IntType(NumericMixin[int]):
    @override
    def _parse(self, raw):
        value = int(raw)
        if value != float(raw):
            raise ValueError(f"The value {raw!r} is not a valid integer.")
        return value


class FloatType(NumericMixin[float]):
    @override
    def _parse(self, raw):
        return float(raw)
