"""Shell command processing for the VFS emulator."""

from dataclasses import dataclass
from typing import Callable

from .parser import ParseError, parse_command


@dataclass(frozen=True)
class CommandResult:
    """Store the result of one command execution."""

    output: str = ""
    should_exit: bool = False


class Shell:
    """Process commands supported by the emulator."""

    def __init__(self) -> None:
        """Create a shell with the stage 1 commands."""
        self.commands: dict[str, Callable[[list[str]], str]] = {
            "ls": self._ls,
            "cd": self._cd,
        }

    def execute_line(self, line: str) -> CommandResult:
        """Parse and execute one input line."""
        try:
            command, args = parse_command(line)
        except ParseError as exc:
            return CommandResult(f"Ошибка: {exc}")

        if not command:
            return CommandResult()

        if command == "exit":
            return CommandResult(should_exit=True)

        handler = self.commands.get(command)
        if handler is None:
            message = f"Ошибка: неизвестная команда '{command}'."
            return CommandResult(message)

        return CommandResult(handler(args))

    def _ls(self, args: list[str]) -> str:
        """Execute the ls stage 1 stub."""
        return self._format_stub("ls", args)

    def _cd(self, args: list[str]) -> str:
        """Execute the cd stage 1 stub."""
        return self._format_stub("cd", args)

    @staticmethod
    def _format_stub(command: str, args: list[str]) -> str:
        """Format a stub command result."""
        return " ".join([command, *args])
