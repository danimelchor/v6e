import pytest

import v6e as v


def test_custom_parse_works():
    my_val = v.int(msg="Failed to parse int... boo!")

    with pytest.raises(ValueError) as e_info:
        my_val.parse("a")

    assert e_info.value.args[0] == "Failed to parse int... boo!"


def test_custom_message_works():
    my_val = v.int().lt(5, msg="Woopsieeee! Less than 5 please...")

    with pytest.raises(ValueError) as e_info:
        my_val.parse(6)

    assert e_info.value.args[0] == "Woopsieeee! Less than 5 please..."
