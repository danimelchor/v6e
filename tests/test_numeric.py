from __future__ import annotations

import v6e as v
from tests.util import (
    V6eFullTestCase,
    V6eTest,
    V6eTestCase,
    generate_tests,
)

all_test_cases = generate_tests(
    V6eTest(
        fn=v.int().max(5),
        cases=[
            V6eTestCase(4, check=True),
            V6eTestCase(5, check=True),
            V6eTestCase(6, check=False),
        ],
    ),
    V6eTest(
        fn=v.int().min(5),
        cases=[
            V6eTestCase(4, check=False),
            V6eTestCase(5, check=True),
            V6eTestCase(6, check=True),
        ],
    ),
    V6eTest(
        fn=v.int().gt(5),
        cases=[
            V6eTestCase(4, check=False),
            V6eTestCase(5, check=False),
            V6eTestCase(6, check=True),
        ],
    ),
    V6eTest(
        fn=v.int().lt(5),
        cases=[
            V6eTestCase(4, check=True),
            V6eTestCase(5, check=False),
            V6eTestCase(6, check=False),
        ],
    ),
    V6eTest(
        fn=v.int().positive(),
        cases=[
            V6eTestCase(-1, check=False),
            V6eTestCase(0, check=False),
            V6eTestCase(1, check=True),
        ],
    ),
    V6eTest(
        fn=v.int().negative(),
        cases=[
            V6eTestCase(-1, check=True),
            V6eTestCase(0, check=False),
            V6eTestCase(1, check=False),
        ],
    ),
    V6eTest(
        fn=v.int().nonnegative(),
        cases=[
            V6eTestCase(-1, check=False),
            V6eTestCase(0, check=True),
            V6eTestCase(1, check=True),
        ],
    ),
    V6eTest(
        fn=v.int().nonpositive(),
        cases=[
            V6eTestCase(-1, check=True),
            V6eTestCase(0, check=True),
            V6eTestCase(1, check=False),
        ],
    ),
    V6eTest(
        fn=v.int().multiple_of(3),
        cases=[
            V6eTestCase(-3, check=True),
            V6eTestCase(-1, check=False),
            V6eTestCase(0, check=True),
            V6eTestCase(3, check=True),
            V6eTestCase(6, check=True),
            V6eTestCase(5, check=False),
        ],
    ),
)


@all_test_cases
def test_all(test: V6eFullTestCase):
    pass
