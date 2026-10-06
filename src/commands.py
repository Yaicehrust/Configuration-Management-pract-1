"""Command implementations for the VFS shell."""

import calendar
from datetime import date


BYTES_PER_UNIT = 1024
MIN_MONTH = 1
MAX_MONTH = 12
ONE_ARG = 1
TWO_ARGS = 2


class CommandError(ValueError):
    """Raised when command arguments are invalid."""


def _split_option(args: list[str], option: str) -> tuple[bool, list[str]]:
    """Extract one short option from arguments."""
    enabled = option in args
    remaining = [arg for arg in args if arg != option]
    return enabled, remaining


def format_size(value: int, human: bool) -> str:
    """Format a byte count."""
    if not human:
        return str(value)
    units = ["B", "K", "M", "G", "T"]
    number = float(value)
    index = 0
    last_unit = len(units) - ONE_ARG
    while number >= BYTES_PER_UNIT and index < last_unit:
        number /= BYTES_PER_UNIT
        index += ONE_ARG
    return f"{number:.1f}{units[index]}"


def command_ls(vfs, current, args: list[str]) -> str:
    """List files and directories in the selected path."""
    long_format, remaining = _split_option(args, "-l")
    if len(remaining) > ONE_ARG:
        raise CommandError("Использование: ls [-l] [PATH]")
    target_path = remaining[0] if remaining else "."
    target = vfs.resolve(target_path, current)
    if target is None:
        raise CommandError("Путь не найден.")
    if not target.is_dir:
        return _format_ls_node(target, long_format)
    lines = [
        _format_ls_node(node, long_format)
        for node in target.children.values()
    ]
    return "\n".join(sorted(lines))


def _format_ls_node(node, long_format: bool) -> str:
    """Format one node for ls."""
    if not long_format:
        return node.name
    kind = "d" if node.is_dir else "-"
    return f"{kind} {node.size:>6} {node.owner:<12} {node.name}"


def command_cd(vfs, current, args: list[str]):
    """Change the current virtual directory."""
    if len(args) > ONE_ARG:
        raise CommandError("Использование: cd [PATH]")
    target_path = "." if not args else args[0]
    target = vfs.resolve(target_path, current)
    if target is None or not target.is_dir:
        raise CommandError("Каталог не найден.")
    return target


def command_du(vfs, current, args: list[str]) -> str:
    """Display recursive directory sizes."""
    summary, remaining = _split_option(args, "-s")
    human, remaining = _split_option(remaining, "-h")
    if len(remaining) > ONE_ARG:
        raise CommandError("Использование: du [-s] [-h] [PATH]")
    target_path = remaining[0] if remaining else "."
    target = vfs.resolve(target_path, current)
    if target is None:
        raise CommandError("Путь не найден.")
    if summary or not target.is_dir:
        return _format_du_entry(vfs, target, human)
    nodes = [node for node in vfs.walk(target) if node.is_dir]
    entries = [_format_du_entry(vfs, node, human) for node in nodes]
    return "\n".join(sorted(entries))


def _format_du_entry(vfs, node, human: bool) -> str:
    """Format one du result line."""
    size = format_size(vfs.total_size(node), human)
    return f"{size}\t{vfs.path_of(node)}"


def command_cal(args: list[str]) -> str:
    """Display a calendar."""
    if not args:
        year, month = date.today().year, date.today().month
    elif len(args) == ONE_ARG:
        try:
            year = int(args[0])
        except ValueError as exc:
            raise CommandError(
                "Использование: cal [YEAR] или cal MONTH YEAR"
            ) from exc
        return calendar.calendar(year)
    elif len(args) == TWO_ARGS:
        try:
            month, year = int(args[0]), int(args[ONE_ARG])
        except ValueError as exc:
            raise CommandError("Месяц и год должны быть числами.") from exc
        if month < MIN_MONTH or month > MAX_MONTH:
            raise CommandError("Месяц должен быть от 1 до 12.")
    else:
        raise CommandError("Использование: cal [YEAR | MONTH YEAR]")
    return calendar.month(year, month)
