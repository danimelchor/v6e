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
        fn=[v.float()],
        success_args=[
            -1,
            0,
            1,
            0.1,
            -0.1,
            0.123456,
            "-1",
            "0",
            "1",
            "0.1",
            "-0.1",
            "0.123456",
            True,
            False,
        ],
        failure_args=["a", datetime.now(), timedelta()],
    ),
    V6eTest(
        fn=[v.int()],
        success_args=[-1, 0, 1, "-1", "0", "1", True, False],
        failure_args=[
            0.1,
            -0.1,
            0.123456,
            "0.1",
            "-0.1",
            "0.123456",
            "a",
            datetime.now(),
            timedelta(),
        ],
    ),
    # ----- Running all possible checks -----
    V6eTest(
        fn=[v.int().max(5), v.int().lte(5)],
        success_args=[4, 5],
        failure_args=[6],
    ),
    V6eTest(
        fn=[v.int().min(5), v.int().gte(5)],
        success_args=[5, 6],
        failure_args=[4],
    ),
    V6eTest(
        fn=[v.int().gt(0), v.int().positive()],
        success_args=[1, 2, 3],
        failure_args=[-1, 0],
    ),
    V6eTest(
        fn=[v.int().lt(0), v.int().negative()],
        success_args=[-2, -1],
        failure_args=[0, 1],
    ),
    V6eTest(
        fn=[v.int().nonnegative()],
        success_args=[0, 1],
        failure_args=[-2, -1],
    ),
    V6eTest(
        fn=[v.int().nonpositive()],
        success_args=[-1, 0],
        failure_args=[1, 2],
    ),
    V6eTest(
        fn=[v.int().multiple_of(3)],
        success_args=[-6, -3, 0, 3, 6],
        failure_args=[-4, -2, -1, 1, 2, 4],
    ),
)


@all_test_cases
def test_all(test: V6eCase):
    pass
