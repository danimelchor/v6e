from __future__ import annotations

import v6e as v
from tests.util import (
    V6eCase,
    V6eTest,
    generate_tests,
)


def _validate_earth_age(x: int) -> None:
    if x != 4_543_000_000:
        raise ValueError("The Earth is 4.543 billion years old. Try 4543000000.")


def _capitalize_if_one_word(s: str) -> str:
    if " " in s:
        raise ValueError(f"Value {s} must be a single word")
    return s.capitalize()


all_test_cases = generate_tests(
    V6eTest(
        fn=[v.int().custom(_validate_earth_age)],
        success_args=[4_543_000_000, "4543000000"],
        failure_args=[0],
    ),
    V6eTest(
        fn=[v.str().custom(_capitalize_if_one_word)],
        success_args=["hello", "world!"],
        success_ret_values=["Hello", "World!"],
        failure_args=["two words?", "tHis sHouLd faiL..."],
    ),
)


@all_test_cases
def test_all(test: V6eCase):
    pass
