from __future__ import annotations

from datetime import datetime, timedelta

from v6e.types.base import V6eType


class DateTimeType(V6eType[datetime]):
    pass


class TimeDeltaType(V6eType[timedelta]):
    pass
