from __future__ import annotations

from datetime import datetime, timedelta

import v6e as v
from tests.util import (
    V6eCase,
    V6eTest,
    generate_tests,
)

all_test_cases = generate_tests(
    V6eTest(
        fn=[v.int().gte(4).lte(5) | v.str().regex("^a|b$")],
        success_args=[4, 5, "a", "b"],
        success_ret_values=[4, 5, "a", "b"],
        failure_args=[3, "c", datetime.now(), timedelta()],
    ),
)


@all_test_cases
def test_all(test: V6eCase):
    pass
