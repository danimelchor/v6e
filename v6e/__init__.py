from v6e.exceptions import ValidationException
from v6e.types import base, boolean, calendar, numbers, string

V6eType = base.V6eType

V6eBooleanType = boolean.BoolType
V6eIntType = numbers.IntType
V6eFloatType = numbers.FloatType
V6eStrType = string.StrType
V6eDateTimeType = calendar.DateTimeType
V6eTimeDeltaType = calendar.TimeDeltaType

bool = boolean.BoolType
int = numbers.IntType
float = numbers.FloatType
str = string.StrType
datetime = calendar.DateTimeType
timedelta = calendar.TimeDeltaType

__all__ = [
    "V6eBooleanType",
    "V6eIntType",
    "V6eFloatType",
    "V6eStrType",
    "V6eDateTimeType",
    "V6eTimeDeltaType",
    "ValidationException",
    "bool",
    "int",
    "float",
    "str",
    "datetime",
    "timedelta",
]
