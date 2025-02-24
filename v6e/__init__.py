from v6e.exceptions import ParseException
from v6e.types import utils
from v6e.types.base import V6eType
from v6e.types.boolean import V6eBool
from v6e.types.calendar import V6eDateTime, V6eTimeDelta
from v6e.types.numbers import V6eFloat, V6eInt
from v6e.types.string import V6eStr

bool = utils.alias(V6eBool, "bool")
int = utils.alias(V6eInt, "int")
float = utils.alias(V6eFloat, "float")
str = utils.alias(V6eStr, "str")
datetime = utils.alias(V6eDateTime, "datetime")
timedelta = utils.alias(V6eTimeDelta, "timedelta")

__all__ = [
    "V6eType",
    "V6eBool",
    "V6eInt",
    "V6eFloat",
    "V6eStr",
    "V6eDateTime",
    "V6eTimeDelta",
    "ParseException",
    "bool",
    "int",
    "float",
    "str",
    "datetime",
    "timedelta",
]
