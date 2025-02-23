from __future__ import annotations

import typing as t

from typing_extensions import override

from v6e.types.comparable import ComparableMixin
from v6e.types.utils import parser

Numeric = t.TypeVar("Numeric", bound=int | float)


class NumericMixin(ComparableMixin[Numeric]):
    @parser
    def positive(self, value: Numeric):
        if value <= 0:
            raise ValueError("Value {} must be positive")

    @parser
    def nonpositive(self, value: Numeric):
        if value > 0:
            raise ValueError("Value {} must not be positive")

    @parser
    def negative(self, value: Numeric):
        if value >= 0:
            raise ValueError("Value {} must be negative")

    @parser
    def nonnegative(self, value: Numeric):
        if value < 0:
            raise ValueError("Value {} must not be negative")

    @parser
    def multiple_of(self, value: Numeric, x: Numeric):
        if value % x != 0:
            raise ValueError(
                f"Value {value} must be a multiple of {x}",
            )

    @parser
    def step(self, value: Numeric, x: Numeric):
        if value % x != 0:
            raise ValueError(
                f"Value {value} must be a multiple of {x}",
            )


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
