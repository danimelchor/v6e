from __future__ import annotations

import typing as t

from pytest import mark

from v6e.types.base import V6eType

T = t.TypeVar("T")


class V6eTestCase(t.Generic[T]):
    def __init__(self, *args: t.Any, check: bool):
        self.args = args
        self.check = check


class V6eTest(t.Generic[T]):
    def __init__(self, fn: V6eType[T], cases: list[V6eTestCase[T]]):
        self.fn = fn
        self.cases = cases

    def iter_cases(self) -> t.Generator[V6eFullTestCase, None, None]:
        for case in self.cases:
            yield V6eFullTestCase(
                args=case.args,
                check=case.check,
                fn=self.fn,
            )


class V6eFullTestCase(t.Generic[T]):
    def __init__(self, args: tuple[t.Any, ...] | None, check: bool, fn: V6eType[T]):
        self.args = args
        self.check = check
        self.fn = fn

    def __repr__(self) -> str:
        return f"{self.fn} for {self.args} == {self.check}"

    def run(self) -> bool:
        return self.fn.check(*self.args)


def generate_tests(*tests: V6eTest) -> t.Callable[...]:
    all_test_cases = []
    for test in tests:
        all_test_cases.extend(test.iter_cases())

    def decorator(
        fun: t.Callable[[V6eFullTestCase], None],
    ) -> t.Callable[[V6eFullTestCase], None]:
        @mark.parametrize(
            "test",
            all_test_cases,
            ids=lambda x: str(x),
        )
        def inner(test: V6eFullTestCase):
            fun(test)

        return inner

    return decorator
