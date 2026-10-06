"""Tests for the command parser."""

import unittest

from src.parser import ParseError, parse_command


class ParserTests(unittest.TestCase):
    """Check command line parsing."""

    def test_simple_command(self) -> None:
        """Parse a command with one argument."""
        self.assertEqual(
            parse_command("cd Documents"),
            ("cd", ["Documents"]),
        )

    def test_quoted_argument(self) -> None:
        """Keep a quoted argument as one value."""
        self.assertEqual(
            parse_command('cd "My Documents"'),
            ("cd", ["My Documents"]),
        )

    def test_multiple_arguments(self) -> None:
        """Parse several arguments."""
        self.assertEqual(
            parse_command('ls "My Documents" test.txt'),
            ("ls", ["My Documents", "test.txt"]),
        )

    def test_unclosed_quote(self) -> None:
        """Reject an unclosed quote."""
        with self.assertRaises(ParseError):
            parse_command('cd "My Documents')


if __name__ == "__main__":
    unittest.main()
