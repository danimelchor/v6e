from __future__ import annotations

import re
import typing as t
from datetime import datetime, timedelta

from dateutil.parser import parse
from typing_extensions import override

from v6e.types.base import V6eType


class V6eDateTime(V6eType[datetime]):
    @override
    def parse_raw(self, raw: t.Any) -> datetime:
        return parse(raw)


TIMDELTA_UNITS = {
    ("weeks", "week", "w"): "weeks",
    ("days", "day", "d"): "days",
    ("hours", "hour", "h"): "hours",
    ("minutes", "minute", "m"): "minutes",
    ("seconds", "second", "s"): "seconds",
    ("milliseconds", "millisecond", "ms"): "milliseconds",
    ("microseconds", "microsecond", "us"): "microseconds",
}
TIMDELTA_REGEX = re.compile(r"^(\d+)\s*(\w+)$")


class V6eTimeDelta(V6eType[timedelta]):
    @override
    def parse_raw(self, raw: t.Any) -> timedelta:
        if isinstance(raw, timedelta):
            return raw

        if not isinstance(raw, str):
            raise ValueError(
                f"Cannot parse {raw!r} as timedelta. Expected str or timedelta, got {type(raw).__name__}"
            )

        match = TIMDELTA_REGEX.match(raw)
        if match is None:
            raise ValueError(f"Invalid timedelta {raw!r}.")

        value, unit = match.groups()
        for units in TIMDELTA_UNITS:
            if unit in units:
                return timedelta(**{TIMDELTA_UNITS[units]: int(value)})

        raise ValueError(f"Invalid timedelta {raw!r}.")
