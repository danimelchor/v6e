from __future__ import annotations

import typing as t

import v6e as v

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
DEFAULT = "\033[39m"


def print_title(x: str) -> None:
    print(BLUE + "\n" + x + DEFAULT)


def _pretty_traceback(err: BaseException):
    tb: list[BaseException] = [err]
    while tb[-1].__cause__ is not None:
        tb.append(tb[-1].__cause__)

    lines = []
    for i, e in enumerate(reversed(tb), 1):
        s = "  " * i + f"↳ {RED}{str(e)}{DEFAULT}"
        lines.append(s)
    return "\n".join(lines)


def print_example(parser: v.V6eType, value: t.Any) -> None:
    try:
        result = parser.parse(value)
        print(
            f"Does {value!r} parse with {parser}? {GREEN}True{DEFAULT}\n"
            + f"  ↳ {GREEN}Parsed value: {result!r}{DEFAULT}"
        )
    except Exception as e:
        traceback = _pretty_traceback(e)
        print(f"Does {value!r} parse with {parser}? {RED}False{DEFAULT}\n{traceback}")
