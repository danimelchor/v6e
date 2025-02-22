from v6e.types.boolean import V6eBoolType
from v6e.types.calendar import V6eDateTimeType, V6eTimeDeltaType
from v6e.types.numbers import V6eFloatType, V6eIntType
from v6e.types.string import V6eStrType

# class v:
#     int = V6eIntType
#     float = V6eFloatType
#     str = V6eStrType
#     bool = V6eBoolType
#     datetime = V6eDateTimeType
#     timedelta = V6eTimeDeltaType


def int():
    return V6eIntType()


def float():
    return V6eFloatType()


def str():
    return V6eStrType()


def bool():
    return V6eBoolType()


def datetime():
    return V6eDateTimeType()


def timedelta():
    return V6eTimeDeltaType()
