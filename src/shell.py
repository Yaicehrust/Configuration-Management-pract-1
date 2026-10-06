"""State and command dispatching for the VFS emulator."""

from dataclasses import dataclass
from typing import Callable

from .commands import (
    CommandError,
    command_cal,
    command_cd,
    command_chown,
    command_du,
    command_ls,
)
from .parser import ParseError, parse_command
from .vfs import Vfs, VfsError, VfsNode


ONE_ARG = 1


@dataclass(frozen=True)
class CommandResult:
    """Store command output and shell state changes."""

    output: str = ""
    should_exit: bool = False
    vfs_changed: bool = False


class Shell:
    """Execute supported commands against an in-memory VFS."""

    def __init__(self, vfs: Vfs | None = None) -> None:
        """Create a shell with an optional VFS."""
        self.vfs = vfs or Vfs()
        self.current = self.vfs.root
        self.commands: dict[str, Callable[[list[str]], str]] = {
            "ls": self._ls,
            "cd": self._cd,
            "du": self._du,
            "cal": self._cal,
            "chown": self._chown,
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
        if command == "vfs-load":
            return self._vfs_load(args)
        handler = self.commands.get(command)
        if handler is None:
            return CommandResult(f"Ошибка: неизвестная команда '{command}'.")
        try:
            return CommandResult(handler(args))
        except CommandError as exc:
            return CommandResult(f"Ошибка: {exc}")

    def _ls(self, args: list[str]) -> str:
        """Execute ls."""
        return command_ls(self.vfs, self.current, args)

    def _cd(self, args: list[str]) -> str:
        """Execute cd and update the current directory."""
        self.current = command_cd(self.vfs, self.current, args)
        return ""

    def _du(self, args: list[str]) -> str:
        """Execute du."""
        return command_du(self.vfs, self.current, args)

    def _cal(self, args: list[str]) -> str:
        """Execute cal."""
        return command_cal(args)

    def _chown(self, args: list[str]) -> str:
        """Execute chown."""
        return command_chown(self.vfs, self.current, args)

    @staticmethod
    def _exit(args: list[str]) -> CommandResult:
        """Terminate the shell when exit has no arguments."""
        if args:
            return CommandResult("Ошибка: exit не принимает аргументы.")
        return CommandResult(should_exit=True)

    def _vfs_load(self, args: list[str]) -> CommandResult:
        """Load another VFS from disk into memory."""
        if len(args) != ONE_ARG:
            return CommandResult("Ошибка: Использование: vfs-load PATH")
        try:
            new_vfs = Vfs.from_csv(args[0])
        except VfsError as exc:
            return CommandResult(f"Ошибка: {exc}")
        self.vfs = new_vfs
        self.current = new_vfs.root
        return CommandResult(
            f"VFS загружена: {new_vfs.name}",
            vfs_changed=True,
        )
