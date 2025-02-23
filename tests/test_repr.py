from pytest import mark

import v6e as v


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
    ],
)
def test_base_class_repr(validation, expected):
    assert str(validation) == expected
