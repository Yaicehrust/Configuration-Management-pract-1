"""Startup script execution for the VFS emulator."""

from pathlib import Path
from typing import Callable


def load_script(path: str) -> list[str]:
    """Load command lines from a startup script."""
    source = Path(path)
    if not source.is_file():
        raise OSError(f"Скрипт не найден: {path}")
    return source.read_text(encoding="utf-8").splitlines()


def run_script(
    path: str,
    execute: Callable[[str], tuple[str, bool]],
    write: Callable[[str], None],
) -> None:
    """Run script lines and display both input and output."""
    for line in load_script(path):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        write(f"> {stripped}")
        output, should_exit = execute(stripped)
        if output:
            write(output)
        if should_exit:
            break
