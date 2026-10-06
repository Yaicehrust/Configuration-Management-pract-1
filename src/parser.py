"""Command parser for the VFS shell emulator."""

import shlex


class ParseError(ValueError):
    """Raised when a command line cannot be parsed."""


def parse_command(line: str) -> tuple[str, list[str]]:
    """Parse a command line into a name and its arguments."""
    if not line.strip():
        return "", []
    try:
        parts = shlex.split(line)
    except ValueError as exc:
        raise ParseError("Незакрытая кавычка.") from exc
    return parts[0], parts[1:]
