from __future__ import annotations

import typing as t
from abc import abstractmethod


class _HasLt(t.Protocol):
    @abstractmethod
    def __lt__(self, other: t.Self, /) -> bool: ...


class _HasGt(t.Protocol):
    def __gt__(self, other: t.Self, /) -> bool: ...


class _HasLte(t.Protocol):
    def __le__(self, other: t.Self, /) -> bool: ...


class _HasGte(t.Protocol):
    def __ge__(self, other: t.Self, /) -> bool: ...


HasLt = t.TypeVar("HasLt", bound=_HasLt)
HasGt = t.TypeVar("HasGt", bound=_HasGt)
HasLte = t.TypeVar("HasLte", bound=_HasLte)
HasGte = t.TypeVar("HasGte", bound=_HasGte)
