from __future__ import annotations

from datetime import datetime, timedelta

from v6e.types.base import V6eType


class V6eDateTime(V6eType[datetime]):
    pass


class V6eTimeDelta(V6eType[timedelta]):
    pass
