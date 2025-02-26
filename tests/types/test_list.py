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
        fn=[v.list(v.str())],
        success_args=[["1", "2", "3"]],
        failure_args=[
            [1, 2, 3],
            [1, 2, "3"],
            ["1", "2", 3],
        ],
    ),
    V6eTest(
        fn=[v.list(v.int().gte(5)), v.int().gte(5).list()],
        success_args=[[5, 6, 7]],
        failure_args=[
            [1, 2, 3],
            [1, 2, "3"],
            ["1", "2", 3],
            ["1", "2", "3"],
        ],
    ),
    V6eTest(
        fn=[v.list(v.int()).max(2)],
        success_args=[[1, 2], [1], []],
        failure_args=[[1, 2, 3]],
    ),
    V6eTest(
        fn=[v.list(v.int()).min(2)],
        success_args=[[1, 2], [1, 2, 3]],
        failure_args=[[1], []],
    ),
    V6eTest(
        fn=[v.list(v.int()).length(3)],
        success_args=[[1, 2, 3]],
        failure_args=[[1, 2], [1, 2, 3, 4]],
    ),
    V6eTest(
        fn=[v.list(v.int()).contains(5)],
        success_args=[[5], [1, 2, 5]],
        failure_args=[[1, 2], [1, 2, 3, 4], []],
    ),
)


@all_test_cases
def test_all(test: V6eCase):
    pass
