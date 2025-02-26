from __future__ import annotations

import typing as t

from v6e.exceptions import ParseException

T = t.TypeVar("T")


class V6eResult(t.Generic[T]):
    __slots__ = ("_result", "_error_message", "_cause")

    def __init__(
        self,
        result: T | None = None,
        error_message: str | None = None,
        _cause: Exception | None = None,
    ) -> None:
        self._result = result
        self._error_message = error_message
        self._cause = _cause

    def is_err(self) -> bool:
        return self._error_message is not None

    def is_ok(self) -> bool:
        return self._error_message is None

    @property
    def result(self) -> T:
        assert self._result is not None
        return self._result

    def get_exception(self) -> ParseException:
        assert self._error_message is not None
        exc = ParseException(self._error_message)
        if self._cause:
            exc.__cause__ = self._cause
        return exc
