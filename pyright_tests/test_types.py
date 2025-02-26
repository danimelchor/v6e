"""
This file is not a real python test. It's meant to be executed with
pyright and will ensure that v6e's types are inferred correctly.
"""

import typing as t
from datetime import timezone

import v6e as v

# ---- Base types ----
t.assert_type(v.int(), v.V6eInt)
t.assert_type(v.int().gt(1), v.V6eInt)

t.assert_type(v.float(), v.V6eFloat)
t.assert_type(v.float().lt(1), v.V6eFloat)

t.assert_type(v.str(), v.V6eStr)
t.assert_type(v.str().contains("a"), v.V6eStr)

t.assert_type(v.bool(), v.V6eBool)
t.assert_type(v.bool().is_false(), v.V6eBool)

t.assert_type(v.datetime(), v.V6eDateTime)
t.assert_type(v.datetime().tz(timezone.utc), v.V6eDateTime)

t.assert_type(v.timedelta(), v.V6eTimeDelta)

t.assert_type(v.dict(a=v.int()), v.V6eDict)

t.assert_type(v.struct(a=v.int(), b=v.bool()), v.V6eStruct)

t.assert_type(v.list(v.int()), v.V6eList[int])


# ---- Custom ----
def double(a: int) -> int:
    return a * 2


t.assert_type(v.int().custom(double), v.V6eInt)

# ---- Unions ----
t.assert_type(v.int().gt(4) | v.str().starts_with("foo"), v.V6eUnion[int, str])
