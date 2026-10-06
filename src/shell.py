"""State and command processing for the VFS emulator."""

from dataclasses import dataclass
from typing import Callable

from .parser import ParseError, parse_command
from .vfs import Vfs, VfsError, VfsNode


@dataclass(frozen=True)
class CommandResult:
    """Store command output and state changes."""

    output: str = ""
    should_exit: bool = False
    vfs_changed: bool = False


class Shell:
    """Execute stage 3 commands against an in-memory VFS."""

    def __init__(self, vfs: Vfs | None = None) -> None:
        """Create a shell with the supplied VFS."""
        self.vfs = vfs or Vfs()
        self.current = self.vfs.root
        self.commands: dict[str, Callable[[list[str]], str]] = {
            "ls": self._ls,
            "cd": self._cd,
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
            if args:
                return CommandResult("Ошибка: exit не принимает аргументы.")
            return CommandResult(should_exit=True)
        handler = self.commands.get(command)
        if handler is None:
            return CommandResult(f"Ошибка: неизвестная команда '{command}'.")
        return CommandResult(handler(args))

    def _ls(self, args: list[str]) -> str:
        """Run the ls stub."""
        return " ".join(["ls", *args])

    def _cd(self, args: list[str]) -> str:
        """Run the cd stub."""
        return " ".join(["cd", *args])
