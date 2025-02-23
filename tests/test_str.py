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
        fn=[v.str()],
        success_args=["a"],
        failure_args=[1, False, datetime.now(), timedelta()],
    ),
    # ----- Running comparable checks -----
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
    # ----- Running sequence checks -----
    V6eTest(
        fn=[v.str().length(5)],
        success_args=["abcde"],
        failure_args=["acbd", "abcdef"],
    ),
    V6eTest(
        fn=[v.str().contains("a")],
        success_args=["a", "abc", "cba"],
        failure_args=["cbd", "bc", ""],
    ),
    # ----- Running string checks -----
    V6eTest(
        fn=[v.str().starts_with("a")],
        success_args=["a", "abc"],
        failure_args=["cbda", "bca", "ba"],
    ),
    V6eTest(
        fn=[v.str().ends_with("a")],
        success_args=["a", "bca"],
        failure_args=["abcd", "bac", "ac"],
    ),
    V6eTest(
        fn=[v.str().regex(r"^[0-9a-z]+$")],
        success_args=["abc123", "123", "abc", "a"],
        failure_args=["abc123@", "abc-123", ""],
    ),
    V6eTest(
        fn=[v.str().email()],
        success_args=["abc@efg.com", "dmh672@gmail.com", "wow@pm.me"],
        failure_args=["abc123@", "@gmail.com", "pm.me.com"],
    ),
    V6eTest(
        fn=[v.str().uuid()],
        success_args=["0123abcd-01ab-ab01-0a1b-0a1b2c3d4e5f"],
        failure_args=["0123abcd-01ab-ab01-0a1b-0a1b2c3d4e5"],
    ),
)


@all_test_cases
def test_all(test: V6eCase):
    pass
