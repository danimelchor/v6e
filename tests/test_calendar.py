from __future__ import annotations

from datetime import datetime, timedelta, timezone

import v6e as v
from tests.util import (
    V6eCase,
    V6eTest,
    generate_tests,
)
from v6e.types.calendar import TIMDELTA_UNITS

ALL_TIMEDELTAS = [
    f"1{space}{unit}"
    for space in ["", " "]
    for unit_group in TIMDELTA_UNITS
    for unit in unit_group
]

all_test_cases = generate_tests(
    # ----- Running the parsing logic -----
    V6eTest(
        fn=[v.timedelta()],
        success_args=ALL_TIMEDELTAS,
        failure_args=[1, False, datetime.now()],
    ),
    V6eTest(
        fn=[v.datetime()],
        success_args=[
            "2024-01-01T00:00:00",
            "2024-01-01T00:00:00",
            "2024-01-01T00:00:00+00:00",
            "2024-01-01T00:00:00Z",
        ],
        success_ret_values=[
            datetime(2024, 1, 1, 0, 0, 0),
            datetime(2024, 1, 1, 0, 0, 0),
            datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        ],
        failure_args=[1, False, timedelta()],
    ),
    # ----- Running comparable checks -----
    V6eTest(
        fn=[v.datetime().tz(timezone.utc)],
        success_args=[
            datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            datetime(2024, 1, 1, 1, 0, 0, tzinfo=timezone(timedelta(hours=1))),
        ],
        success_ret_values=[
            datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        ],
    ),
)


@all_test_cases
def test_all(test: V6eCase):
    pass
