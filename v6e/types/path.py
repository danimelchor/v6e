from pathlib import Path

from typing_extensions import override

from v6e.types.base import V6eType, parser


class V6ePath(V6eType[Path]):
    @override
    def parse_raw(self, raw):
        if isinstance(raw, Path):
            return raw
        if not isinstance(raw, str):
            raise ValueError(f"The value {raw!r} is not a valid path.")
        return Path(raw)

    @parser
    def exists(self, value: Path, /, msg: str | None = None):
        if not value.exists():
            raise ValueError(f"Path {value} does not exist")

    @parser
    def expanduser(self, value: Path, /, msg: str | None = None):
        return value.expanduser()

    @parser
    def absolute(self, value: Path, /, msg: str | None = None):
        return value.absolute()

    @parser
    def resolve(self, value: Path, /, msg: str | None = None):
        return value.resolve()

    @parser
    def is_dir(self, value: Path, /, msg: str | None = None):
        if not value.is_dir():
            raise ValueError(f"Path {value} is not a directory")

    @parser
    def is_file(self, value: Path, /, msg: str | None = None):
        if not value.is_file():
            raise ValueError(f"Path {value} is not a file")
