import pytest

import v6e as v


def test_parser_as_function():
    validation = v.int().gt(5)
    assert validation(6) == 6
    assert validation("6") == 6

    with pytest.raises(v.ParseException):
        validation(5)
