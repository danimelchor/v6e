from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import v6e as v
from tests.util import (
    V6eCase,
    V6eTest,
    generate_tests,
)

# v.exists()
# v.expanduser()
# v.absolute()
# v.resolve()
# v.is_dir()
# v.is_file()

all_test_cases = generate_tests(
    # ----- Running the parsing logic -----
    V6eTest(
        fn=[v.path()],
        success_args=["./foo.bar"],
        failure_args=[1, False, datetime.now(), timedelta()],
    ),
    # ----- Running path checks -----
    V6eTest(
        fn=[v.path().exists()],
        success_args=[__file__],
        failure_args=["/tmp/does/not/exist"],
    ),
    V6eTest(
        fn=[v.path().absolute()],
        success_args=["/foo/bar"],
    ),
    V6eTest(
        fn=[v.path().is_file()],
        success_args=[__file__],
        failure_args=[Path(__file__).parent],
    ),
    V6eTest(
        fn=[v.path().is_dir()],
        success_args=[Path(__file__).parent],
        failure_args=[__file__],
    ),
)


@all_test_cases
def test_all(test: V6eCase):
    pass
