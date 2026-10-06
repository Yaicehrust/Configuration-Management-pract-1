"""State and command dispatching for the VFS emulator."""

from dataclasses import dataclass
from typing import Callable

from .commands import (
    CommandError,
    command_cal,
    command_cd,
    command_du,
    command_ls,
)
from .parser import ParseError, parse_command
from .vfs import Vfs, VfsNode


@dataclass(frozen=True)
class CommandResult:
    """Store command output and shell state changes."""

    output: str = ""
    should_exit: bool = False
    vfs_changed: bool = False


class Shell:
    """Execute commands against an in-memory VFS."""

    def __init__(self, vfs: Vfs | None = None) -> None:
        """Create a shell with the supplied VFS."""
        self.vfs = vfs or Vfs()
        self.current = self.vfs.root
        self.commands: dict[str, Callable[[list[str]], str | VfsNode]] = {
            "ls": self._ls,
            "cd": self._cd,
            "du": self._du,
            "cal": self._cal,
        }

    def execute_line(self, line: str) -> CommandResult:
        """Parse and execute one command line."""
        try:
            command, args = parse_command(line)
        except ParseError as exc:
            return CommandResult(f"Ошибка: {exc}")
        if not command:
            return CommandResult()
        if command == "exit":
            return self._exit(args)
        handler = self.commands.get(command)
        if handler is None:
            return CommandResult(f"Ошибка: неизвестная команда '{command}'.")
        try:
            value = handler(args)
        except CommandError as exc:
            return CommandResult(f"Ошибка: {exc}")
        if isinstance(value, VfsNode):
            self.current = value
            return CommandResult()
        return CommandResult(value)

    def _ls(self, args: list[str]) -> str:
        """Execute ls."""
        return command_ls(self.vfs, self.current, args)

    def _cd(self, args: list[str]) -> VfsNode:
        """Execute cd and return the new current directory."""
        return command_cd(self.vfs, self.current, args)

    def _du(self, args: list[str]) -> str:
        """Execute du."""
        return command_du(self.vfs, self.current, args)

    def _cal(self, args: list[str]) -> str:
        """Execute cal."""
        return command_cal(args)

    @staticmethod
    def _exit(args: list[str]) -> CommandResult:
        """Exit when no arguments are provided."""
        if args:
            return CommandResult("Ошибка: exit не принимает аргументы.")
        return CommandResult(should_exit=True)
