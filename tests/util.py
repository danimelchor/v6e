from __future__ import annotations

import typing as t
from dataclasses import dataclass
from itertools import product

from pytest import mark

import v6e as v

T = t.TypeVar("T")


@t.final
@dataclass
class V6eTest(t.Generic[T]):
    fn: list[v.V6eType[T]]
    success_args: list[t.Any] | None = None
    success_ret_values: list[T] | None = None
    failure_args: list[t.Any] | None = None
    exc: t.Type[Exception] = v.ParseException

    def __post_init__(self):
        if self.success_args and self.success_ret_values:
            assert len(self.success_args) == len(self.success_ret_values)

    def iter_cases(self) -> t.Generator[V6eCase, None, None]:
        fns = self.fn if isinstance(self.fn, list) else [self.fn]

        if self.success_args is not None:
            ret_values = self.success_ret_values or [None] * len(self.success_args)
            args_with_ret = zip(self.success_args, ret_values)
            for (arg, ret), fn in product(args_with_ret, fns):
                yield V6eCase(fn=fn, arg=arg, ret_value=ret)

        if self.failure_args is not None:
            for arg, fn in product(self.failure_args, fns):
                yield V6eCase(fn=fn, arg=arg, fails=True, exc=self.exc)


@t.final
@dataclass
class V6eCase(t.Generic[T]):
    fn: v.V6eType[T]
    arg: t.Any | None = None
    ret_value: T | None = None
    fails: bool = False
    exc: t.Type[Exception] = v.ParseException

    def __repr__(self) -> str:
        result = "fails" if self.fails else "succeeds"
        return f"{self.fn} for {self.arg} {result}"

    def run(self):
        parse_res = self.fn.safe_parse(self.arg)

        if not self.fails and parse_res.is_err():
            raise AssertionError(
                f"{self.fn} for {self.arg!r} failed but was expected to pass"
            ) from parse_res.get_exception()

        if self.fails and parse_res.is_ok():
            raise AssertionError(
                f"{self.fn} for {self.arg!a} was expected fail but it did not"
            )

        if self.ret_value and parse_res.result != self.ret_value:
            raise AssertionError(
                f"{self.fn} for {self.arg!a} was expected to return {self.ret_value!r} but"
                + f" it instead returned {parse_res.result!r}",
            )


def generate_tests(*tests: V6eTest) -> t.Callable[...]:
    all_test_cases = []
    for test in tests:
        all_test_cases.extend(test.iter_cases())

    def decorator(
        _fun: t.Callable[[V6eCase], None],
    ) -> t.Callable[[V6eCase], None]:
        @mark.parametrize(
            "test",
            all_test_cases,
            ids=lambda x: str(x),
        )
        def inner(test: V6eCase):
            test.run()

        return inner

    return decorator
