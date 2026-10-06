"""Tests for command-line configuration."""

import unittest

from src.config import AppConfig, parse_args


class ConfigTests(unittest.TestCase):
    """Check supported startup parameters."""

    def test_defaults(self) -> None:
        """Allow the application to start without parameters."""
        self.assertEqual(parse_args([]), AppConfig())

    def test_paths(self) -> None:
        """Parse VFS and script paths."""
        config = parse_args(["--vfs", "a.csv", "--script", "b.txt"])
        self.assertEqual(config.vfs_path, "a.csv")
        self.assertEqual(config.script_path, "b.txt")


if __name__ == "__main__":
    unittest.main()
