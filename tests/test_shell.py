"""Tests for shell commands."""

import unittest

from src.shell import Shell
from src.vfs import Vfs


class ShellTests(unittest.TestCase):
    """Check stage 4 shell behavior."""

    def setUp(self) -> None:
        """Create a VFS from the nested fixture."""
        self.shell = Shell(Vfs.from_csv("data/vfs/nested.csv"))

    def test_ls(self) -> None:
        """List a directory."""
        result = self.shell.execute_line("ls")
        self.assertIn("home", result.output)

    def test_cd_and_parent(self) -> None:
        """Navigate with cd and parent paths."""
        self.shell.execute_line("cd /home/user")
        self.shell.execute_line("cd ..")
        self.assertEqual(
            self.shell.vfs.path_of(self.shell.current),
            "/home",
        )

    def test_du(self) -> None:
        """Calculate recursive sizes."""
        result = self.shell.execute_line("du -s -h /home")
        self.assertIn("/home", result.output)

    def test_cal(self) -> None:
        """Generate a calendar for October 2026."""
        result = self.shell.execute_line("cal 10 2026")
        self.assertIn("October", result.output)

    def test_error(self) -> None:
        """Report invalid paths and commands."""
        self.assertIn(
            "Каталог не найден",
            self.shell.execute_line("cd /missing").output,
        )
        self.assertIn(
            "неизвестная команда",
            self.shell.execute_line("unknown").output,
        )


if __name__ == "__main__":
    unittest.main()
