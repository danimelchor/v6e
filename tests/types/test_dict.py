from __future__ import annotations

import v6e as v
from tests.util import (
    V6eCase,
    V6eTest,
    generate_tests,
)

all_test_cases = generate_tests(
    # ----- Running the parsing logic -----
    V6eTest(
        fn=[v.dict(a=v.int().gt(5) | v.int().lt(1), b=v.bool().is_true())],
        success_args=[
            {"a": 6, "b": True},
            {"a": 0, "b": True},
            {"a": 0, "b": True, "extra": None},
        ],
        success_ret_values=[
            {"a": 6, "b": True},
            {"a": 0, "b": True},
            {"a": 0, "b": True},
        ],
        failure_args=[
            {},
            {"a": 6},
            {"b": True},
            {"a": "a", "b": True},
            {"a": 6, "b": False},
            {"a": "a", "b": "b"},
        ],
    ),
)


@all_test_cases
def test_all(test: V6eCase):
    pass
