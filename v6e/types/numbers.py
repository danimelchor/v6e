from __future__ import annotations

import typing as t

from typing_extensions import override

from v6e.types.comparable import V6eComparableMixin
from v6e.types.utils import parser

Numeric = t.TypeVar("Numeric", bound=int | float)


class V6eNumericMixin(V6eComparableMixin[Numeric]):
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


class V6eInt(V6eNumericMixin[int]):
    @override
    def _parse(self, raw):
        value = int(raw)
        if value != float(raw):
            raise ValueError(f"The value {raw!r} is not a valid integer.")
        return value


class V6eFloat(V6eNumericMixin[float]):
    @override
    def _parse(self, raw):
        return float(raw)
