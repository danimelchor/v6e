from __future__ import annotations

from datetime import datetime

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
    # ----- Running comparable checks -----
)


@all_test_cases
def test_all(test: V6eCase):
    pass
