from __future__ import annotations

import re
import typing as t
from abc import ABC, abstractmethod

from typing_extensions import override

import v6e.bounds as b

T = t.TypeVar("T")


class ValidationException(Exception):
    pass


class Validation(ABC, t.Generic[T]):
    @abstractmethod
    def rule(self, x: T) -> None: ...

    def ensure(self, x: T):
        self.rule(x)

    def __call__(self, x: T) -> bool:
        try:
            self.rule(x)
        except ValidationException:
            return False
        return True

    def __and__(self, other: Validation[T]) -> _Intersection[T]:
        return _Intersection(self, other)

    def __or__(self, other: Validation[T]) -> _Union[T]:
        return _Union(self, other)

    @override
    def __repr__(self):
        display_vars = [
            f"{k}={v}" for k, v in vars(self).items() if not k.startswith("_")
        ]
        joined = ", ".join(display_vars)
        return f"{self.__class__.__name__}({joined})"


class Custom(Validation[T]):
    def __init__(self, func: t.Callable[[T], None]):
        self.func = func
        super().__init__()

    @override
    def rule(self, x):
        try:
            self.func(x)
        except Exception as e:
            raise ValidationException(str(e))


class _Intersection(Validation[T]):
    def __init__(self, left: Validation[T], right: Validation[T]):
        self.left = left
        self.right = right
        super().__init__()

    @override
    def rule(self, x):
        left_err = right_err = None

        try:
            self.left.ensure(x)
        except ValidationException as e:
            left_err = e

        try:
            self.right.ensure(x)
        except ValidationException as e:
            right_err = e

        if left_err and right_err:
            raise ValidationException(f"{left_err} and {right_err}")
        if left_err:
            raise left_err
        if right_err:
            raise right_err

    @override
    def __repr__(self):
        return f"{self.left} & {self.right}"


class _Union(Validation[T]):
    def __init__(self, left: Validation[T], right: Validation[T]):
        self.left = left
        self.right = right
        super().__init__()

    @override
    def rule(self, x):
        left_err = right_err = None

        try:
            self.left.ensure(x)
        except ValidationException as e:
            left_err = e

        try:
            self.right.ensure(x)
        except ValidationException as e:
            right_err = e

        if left_err and right_err:
            raise ValidationException(f"{left_err} or {right_err}")

    @override
    def __repr__(self):
        return f"{self.left} | {self.right}"


class Range(Validation[b.HasLte]):
    def __init__(self, start: b.HasLte, end: b.HasLte):
        self.start = start
        self.end = end
        super().__init__()

    @override
    def rule(self, x):
        if not self.start <= x <= self.end:
            raise ValidationException(
                f"Value must be between {self.start} and {self.end} (got {x})"
            )


class Lt(Validation[b.HasLt]):
    def __init__(self, limit: b.HasLt):
        self.limit = limit
        super().__init__()

    @override
    def rule(self, x):
        if not x < self.limit:
            raise ValidationException(f"Value must be less than {self.limit} (got {x})")


class Lte(Validation[b.HasLte]):
    def __init__(self, limit: b.HasLte):
        self.limit = limit
        super().__init__()

    @override
    def rule(self, x):
        if not x <= self.limit:
            raise ValidationException(
                f"Value must be less than or equal to {self.limit} (got {x})"
            )


class Gt(Validation[b.HasGt]):
    def __init__(self, limit: b.HasGt):
        self.limit = limit
        super().__init__()

    @override
    def rule(self, x):
        if not x > self.limit:
            raise ValidationException(
                f"Value must be greater than {self.limit} (got {x})"
            )


class Gte(Validation[b.HasGte]):
    def __init__(self, limit: b.HasGte):
        self.limit = limit
        super().__init__()

    @override
    def rule(self, x):
        if not x >= self.limit:
            raise ValidationException(
                f"Value must be greater than or equal to {self.limit} (got {x})"
            )


class StartsWith(Validation[str]):
    def __init__(self, prefix: str):
        self.prefix = prefix
        super().__init__()

    @override
    def rule(self, x):
        if not x.startswith(self.prefix):
            raise ValidationException(
                f"Value must start with {self.prefix!r} (got {x!r})"
            )


class EndsWith(Validation[str]):
    def __init__(self, suffix: str):
        self.suffix = suffix
        super().__init__()

    @override
    def rule(self, x):
        if not x.endswith(self.suffix):
            raise ValidationException(
                f"Value must end with {self.suffix!r} (got {x!r})"
            )


class ReMatch(Validation[str]):
    def __init__(self, pattern: str):
        self.pattern = re.compile(pattern)
        super().__init__()

    @override
    def rule(self, x):
        if not self.pattern.match(x):
            raise ValidationException(
                f"Value must match pattern {self.pattern!r} (got {x!r})"
            )


class ReSearch(Validation[str]):
    def __init__(self, pattern: str):
        self.pattern = re.compile(pattern)
        super().__init__()

    @override
    def rule(self, x):
        if not self.pattern.search(x):
            raise ValidationException(
                f"Value must contain pattern {self.pattern!r} (got {x!r})"
            )


class Choices(Validation[T]):
    def __init__(self, choices: t.Sequence[T]):
        self.choices = choices
        super().__init__()

    @override
    def rule(self, x):
        if x not in self.choices:
            raise ValidationException(f"Value must be one of {self.choices} (got {x})")


ValidationType: t.TypeAlias = t.Callable[[T], None] | Validation[T]


def parse_validation(validation: ValidationType[T]) -> Validation[T]:
    # NOTE: We unfortunately cannot match validation to Validation[T]
    # so we need a cast
    if isinstance(validation, Validation):
        return t.cast(Validation[T], validation)

    return Custom(validation)
