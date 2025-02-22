from __future__ import annotations

from datetime import datetime, timedelta

from v6e.types.base import V6eType


class V6eDateTimeType(V6eType[datetime]):
    pass


class V6eTimeDeltaType(V6eType[timedelta]):
    pass
