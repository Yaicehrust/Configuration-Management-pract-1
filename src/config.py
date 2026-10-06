"""Command-line configuration for the emulator."""

from argparse import ArgumentParser
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Store parameters passed to the application."""

    vfs_path: str | None = None
    script_path: str | None = None


def parse_args(args: list[str] | None = None) -> AppConfig:
    """Parse supported command-line parameters."""
    parser = ArgumentParser(description="VFS shell emulator")
    parser.add_argument("--vfs", help="path to VFS CSV file")
    parser.add_argument("--script", help="path to startup script")
    values = parser.parse_args(args)
    return AppConfig(values.vfs, values.script)
