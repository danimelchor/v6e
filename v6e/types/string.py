import re

from typing_extensions import override

from v6e.types.comparable import ComparableMixin
from v6e.types.sequences import SequenceMixin
from v6e.types.utils import parser

EMAIL = re.compile(
    r"^(?!\.)(?!.*\.\.)([A-Z0-9_'+\-\.]*)[A-Z0-9_+-]@([A-Z0-9][A-Z0-9\-]*\.)+[A-Z]{2,}$",
    flags=re.IGNORECASE,
)
UUID = re.compile(
    r"^[0-9A-F]{8}\b-[0-9A-F]{4}\b-[0-9A-F]{4}\b-[0-9A-F]{4}\b-[0-9A-F]{12}$",
    flags=re.IGNORECASE,
)


class StrType(ComparableMixin[str], SequenceMixin[str]):
    @override
    def _parse(self, raw):
        if not isinstance(raw, str):
            raise ValueError(f"The value {raw!r} is not a valid string.")
        return raw

    @parser
    def regex(self, value: str, pattern: str):
        if re.search(pattern, value) is not None:
            raise ValueError(
                f"The string {value} did not match the pattern {pattern!r}"
            )

    @parser
    def email(self, value: str):
        if EMAIL.match(value) is not None:
            raise ValueError(f"The string {value} is not a valid email")

    @parser
    def uuid(self, value: str):
        if UUID.match(value) is not None:
            raise ValueError(f"The string {value} is not a valid uuid")
