from __future__ import annotations

from datetime import datetime, timedelta

import v6e as v
from tests.util import (
    V6eCase,
    V6eTest,
    generate_tests,
)
from v6e.types.boolean import FALSE_BOOL_STR_LITERALS, TRUE_BOOL_STR_LITERALS

all_test_cases = generate_tests(
    # ----- Running the parsing logic -----
    V6eTest(
        fn=[v.bool()],
        success_args=[
            True,
            False,
            0,
            1,
            *TRUE_BOOL_STR_LITERALS,
            *FALSE_BOOL_STR_LITERALS,
        ],
        failure_args=[-1, 3, "a", "", datetime.now(), timedelta()],
    ),
    # ----- Running all possible checks -----
    V6eTest(
        fn=[v.bool().is_true()],
        success_args=[True, 1, *TRUE_BOOL_STR_LITERALS],
        failure_args=[False, 0, *FALSE_BOOL_STR_LITERALS],
    ),
    V6eTest(
        fn=[v.bool().is_false()],
        success_args=[False, 0, *FALSE_BOOL_STR_LITERALS],
        failure_args=[True, 1, *TRUE_BOOL_STR_LITERALS],
    ),
)


@all_test_cases
def test_all(test: V6eCase):
    pass
