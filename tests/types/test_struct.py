from __future__ import annotations

import typing as t
from dataclasses import dataclass

import v6e as v
from tests.util import (
    V6eCase,
    V6eTest,
    generate_tests,
)


@dataclass
class A:
    a: t.Any = None
    b: t.Any = None
    extra: t.Any = None


all_test_cases = generate_tests(
    # ----- Running the parsing logic -----
    V6eTest(
        fn=[v.struct(a=v.int().gt(5) | v.int().lt(1), b=v.bool().is_true())],
        success_args=[
            A(a=6, b=True),
            A(a=0, b=True),
            A(a=0, b=True, extra=5),
        ],
        success_ret_values=[
            A(a=6, b=True),
            A(a=0, b=True),
            A(a=0, b=True, extra=5),
        ],
        failure_args=[
            A(),
            A(a=6),
            A(b=True),
            A(a="a", b=True),
            A(a=6, b=False),
            A(a="a", b="b"),
        ],
    ),
)


@all_test_cases
def test_all(test: V6eCase):
    pass
