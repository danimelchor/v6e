from v6e.exceptions import ParseException
from v6e.types import utils
from v6e.types.base import V6eType, V6eUnion, parser
from v6e.types.boolean import V6eBool
from v6e.types.calendar import V6eDateTime, V6eTimeDelta
from v6e.types.dict import V6eDict
from v6e.types.list import V6eList
from v6e.types.numbers import V6eFloat, V6eInt
from v6e.types.path import V6ePath
from v6e.types.string import V6eStr
from v6e.types.struct import V6eStruct

bool = utils.alias(V6eBool, "bool")
int = utils.alias(V6eInt, "int")
float = utils.alias(V6eFloat, "float")
str = utils.alias(V6eStr, "str")
datetime = utils.alias(V6eDateTime, "datetime")
timedelta = utils.alias(V6eTimeDelta, "timedelta")
dict = utils.alias(V6eDict, "dict")
struct = utils.alias(V6eStruct, "struct")
list = utils.alias(V6eList, "list")
path = utils.alias(V6ePath, "path")

__all__ = [
    "ParseException",
    "V6eBool",
    "V6eDateTime",
    "V6eDict",
    "V6eFloat",
    "V6eInt",
    "V6eList",
    "V6ePath",
    "V6eStr",
    "V6eStruct",
    "V6eTimeDelta",
    "V6eType",
    "V6eUnion",
    "bool",
    "datetime",
    "dict",
    "float",
    "int",
    "list",
    "parser",
    "path",
    "str",
    "struct",
    "timedelta",
]
