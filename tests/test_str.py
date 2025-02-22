from __future__ import annotations

from datetime import datetime, timedelta

import v6e as v
from tests.util import (
    V6eCase,
    V6eTest,
    generate_tests,
)

all_test_cases = generate_tests(
    # ----- Running the parsing logic -----
    V6eTest(
        fn=v.str(),
        success_args=["a"],
        failure_args=[1, False, datetime.now(), timedelta()],
    ),
    # ----- Running all possible checks -----
    V6eTest(
        fn=[v.str().max("x"), v.str().lte("x")],
        success_args=["a", "x"],
        failure_args=["z"],
    ),
    V6eTest(
        fn=[v.str().min("b"), v.str().gte("b")],
        success_args=["b", "z"],
        failure_args=["a"],
    ),
    V6eTest(
        fn=[v.str().gt("a")],
        success_args=["b"],
        failure_args=["a"],
    ),
    V6eTest(
        fn=[v.str().lt("b")],
        success_args=["a"],
        failure_args=["b"],
    ),
)


@all_test_cases
def test_all(test: V6eCase):
    pass
