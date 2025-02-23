from pytest import mark

import v6e as v


def _custom_fn(x: int) -> None:
    raise ValueError(f"{x} shall not pass!")


@mark.parametrize(
    "validation,expected",
    [
        (
            v.V6eInt().gte(5).lt(15).multiple_of(5),
            "v6e.V6eInt().gte(5).lt(15).multiple_of(5)",
        ),
        (
            v.str().contains("foo").regex(r"[a-z0-9]{2}"),
            "v6e.str().contains('foo').regex('[a-z0-9]{2}')",
        ),
        (
            v.int().custom(_custom_fn),
            "v6e.int().custom(_custom_fn)",
        ),
    ],
)
def test_base_class_repr(validation, expected):
    assert str(validation) == expected
