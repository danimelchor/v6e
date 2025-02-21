from __future__ import annotations

from pytest import mark

import v6e


@mark.parametrize(
    "input,expected",
    [
        (1, True),
        (2, True),
        (0, False),
        (3, False),
    ],
)
def test_range_validation(input, expected):
    assert v6e.Range(1, 2)(input) == expected


@mark.parametrize(
    "input,expected",
    [
        ("foo1", True),
        ("f1", True),
        ("z1", False),
        ("f", False),
    ],
)
def test_intersection_validation(input, expected):
    val = v6e.ReSearch(r"[0-9]+$") & v6e.StartsWith("f")
    assert val(input) == expected


@mark.parametrize(
    "input,expected",
    [
        ("foo12", True),
        ("z12", True),
        ("ffff", True),
        ("abc", False),
    ],
)
def test_union_validation(input, expected):
    val = v6e.ReSearch(r"[0-9]{2}$") | v6e.StartsWith("f")
    assert val(input) == expected


def test_union_and_intersection():
    val = v6e.ReSearch(r"[0-9]{2}$") | v6e.StartsWith("f") & v6e.EndsWith("2")
    assert val("12")
    assert val("f2")
    assert val("f12")
    assert not val("z2")


@mark.parametrize(
    "input,expected",
    [
        (1, True),
        (2, False),
        (3, False),
    ],
)
def test_choices_validation(input, expected):
    assert v6e.Choices([1])(input) == expected


def _custom_validation(x: int) -> None:
    if x % 3 != 0:
        raise ValueError("Value must be divisible by 3")


@mark.parametrize(
    "input,expected",
    [
        (3, True),
        (6, True),
        (4, False),
        (5, False),
    ],
)
def test_custom_validation(input, expected):
    assert v6e.Custom(_custom_validation)(input) == expected
