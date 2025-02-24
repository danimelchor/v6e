import v6e as v


def test_custom_message_works():
    my_val = v.int().lt(5, msg="Woopsieeee! Less than 5 please...")
