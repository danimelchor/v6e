import typing as t

from typing_extensions import override

from v6e.types.base import V6eType

TRUE_BOOL_STR_LITERALS: set[str] = {"true", "yes", "y"}
FALSE_BOOL_STR_LITERALS: set[str] = {"false", "no", "n"}


class BoolType(V6eType[bool]):
    @override
    def _parse(self, raw):
        if isinstance(raw, str):
            raw_lower = raw.lower()
            if (
                raw_lower not in TRUE_BOOL_STR_LITERALS
                and raw_lower not in FALSE_BOOL_STR_LITERALS
            ):
                both = TRUE_BOOL_STR_LITERALS | FALSE_BOOL_STR_LITERALS
                raise ValueError(
                    f"The string {raw!r} is not valid boolean! The only allowed values are: {both}."
                )
            return raw_lower in TRUE_BOOL_STR_LITERALS

        if isinstance(raw, int | float):
            if raw not in (0, 1):
                raise ValueError(
                    f"The int {raw!r} is not valid boolean! The only allowed values are 0 and 1."
                )
            return bool(raw)

        if not isinstance(raw, bool):
            raise ValueError(f"The value {raw!r} cannot be parsed as a boolean.")

        return raw

    def is_true(self) -> t.Self:
        return self._chain(
            "is_true()",
            lambda x: x,
            "Value {} must be greater true",
        )

    def is_false(self) -> t.Self:
        return self._chain(
            "is_false()",
            lambda x: not x,
            "Value {} must be greater true",
        )
