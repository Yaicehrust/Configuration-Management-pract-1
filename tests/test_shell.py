"""Tests for shell command processing."""

import unittest

from src.shell import Shell


class ShellTests(unittest.TestCase):
    """Check stage 1 shell behavior."""

    def setUp(self) -> None:
        """Create a fresh shell before each test."""
        self.shell = Shell()

    def test_ls_stub(self) -> None:
        """Check the ls stub."""
        result = self.shell.execute_line("ls")
        self.assertEqual(result.output, "ls")
        self.assertFalse(result.should_exit)

    def test_cd_stub_with_quotes(self) -> None:
        """Check cd with a quoted argument."""
        result = self.shell.execute_line('cd "My Documents"')
        self.assertEqual(result.output, "cd My Documents")

    def test_unknown_command(self) -> None:
        """Report an unknown command."""
        result = self.shell.execute_line("hello")
        self.assertIn("неизвестная команда", result.output)

    def test_exit(self) -> None:
        """Request application termination."""
        result = self.shell.execute_line("exit")
        self.assertTrue(result.should_exit)

    def test_empty_line(self) -> None:
        """Ignore an empty command line."""
        result = self.shell.execute_line("   ")
        self.assertEqual(result.output, "")
        self.assertFalse(result.should_exit)


if __name__ == "__main__":
    unittest.main()
