"""Tests for command-line configuration."""

import unittest

from src.config import AppConfig, parse_args


class ConfigTests(unittest.TestCase):
    """Check supported command-line parameters."""

    def test_defaults(self) -> None:
        """Allow startup without parameters."""
        self.assertEqual(parse_args([]), AppConfig())

    def test_paths(self) -> None:
        """Parse VFS and script paths."""
        config = parse_args(["--vfs", "vfs.csv", "--script", "start.txt"])
        self.assertEqual(config.vfs_path, "vfs.csv")
        self.assertEqual(config.script_path, "start.txt")


if __name__ == "__main__":
    unittest.main()
