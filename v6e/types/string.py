import re

from typing_extensions import override

from v6e.types.base import V6eType, parser

EMAIL = re.compile(
    r"^(?!\.)(?!.*\.\.)([A-Z0-9_'+\-\.]*)[A-Z0-9_+-]@([A-Z0-9][A-Z0-9\-]*\.)+[A-Z]{2,}$",
    flags=re.IGNORECASE,
)
UUID = re.compile(
    r"^[0-9A-F]{8}\b-[0-9A-F]{4}\b-[0-9A-F]{4}\b-[0-9A-F]{4}\b-[0-9A-F]{12}$",
    flags=re.IGNORECASE,
)


class V6eStr(V6eType[str]):
    @override
    def parse_raw(self, raw):
        if not isinstance(raw, str):
            raise ValueError(f"The value {raw!r} is not a valid string.")
        return raw

    @parser
    def startswith(self, value: str, x: str, /, msg: str | None = None):
        if not value.startswith(x):
            raise ValueError(
                f"{value} does not start with {x}",
            )

    @parser
    def endswith(self, value: str, x: str, /, msg: str | None = None):
        if not value.endswith(x):
            raise ValueError(
                f"{value} does not start with {x}",
            )

    @parser
    def regex(self, value: str, x: str, /, msg: str | None = None):
        if re.search(x, value) is None:
            raise ValueError(f"The string {value} did not match the pattern {x!r}")

    @parser
    def email(self, value: str, /, msg: str | None = None):
        if EMAIL.match(value) is None:
            raise ValueError(f"The string {value} is not a valid email")

    @parser
    def uuid(self, value: str, /, msg: str | None = None):
        if UUID.match(value) is None:
            raise ValueError(f"The string {value} is not a valid uuid")

    @parser
    def length(self, value: str, x: int, /, msg: str | None = None):
        if len(value) != x:
            raise ValueError(
                f"The length of {value} is not {x} (it's {len(value)})",
            )

    @parser
    def max(self, value: str, x: int, /, msg: str | None = None):
        if len(value) > x:
            raise ValueError(
                f"The length of {value} has to be at most {x} (it's {len(value)})",
            )

    @parser
    def min(self, value: str, x: int, /, msg: str | None = None):
        if len(value) < x:
            raise ValueError(
                f"The length of {value} has to be at least {x} (it's {len(value)})",
            )

    @parser
    def contains(self, value: str, x: str, /, msg: str | None = None):
        if x not in value:
            raise ValueError(
                f"{value} does not contain {x}",
            )

    @parser
    def nonempty(self, value: str, /, msg: str | None = None):
        if len(value) == 0:
            raise ValueError(f"The value {value} is empty")
