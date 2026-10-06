"""Tests for the in-memory VFS."""

import base64
import csv
import tempfile
import unittest

from src.vfs import Vfs, VfsError


class VfsTests(unittest.TestCase):
    """Check CSV loading and nested tree creation."""

    def _write_vfs(self, rows: list[list[str]]) -> str:
        """Create a temporary VFS CSV file."""
        handle = tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", suffix=".csv", delete=False
        )
        with handle:
            writer = csv.writer(handle)
            writer.writerow(Vfs.HEADER)
            writer.writerows(rows)
        return handle.name

    def test_nested_tree(self) -> None:
        """Build and resolve a three-level tree."""
        data = base64.b64encode(b"abc").decode("ascii")
        path = self._write_vfs(
            [
                ["/", "dir", "0", "root", ""],
                ["/home", "dir", "0", "root", ""],
                ["/home/user", "dir", "0", "user", ""],
                ["/home/user/a.txt", "file", "3", "user", data],
            ]
        )
        vfs = Vfs.from_csv(path)
        node = vfs.resolve("/home/user/a.txt")
        self.assertIsNotNone(node)
        self.assertEqual(vfs.total_size(vfs.root), 3)

    def test_missing_file(self) -> None:
        """Reject a missing VFS file."""
        with self.assertRaises(VfsError):
            Vfs.from_csv("missing.csv")

    def test_invalid_base64(self) -> None:
        """Reject invalid Base64 data."""
        path = self._write_vfs(
            [
                ["/", "dir", "0", "root", ""],
                ["/a.bin", "file", "2", "root", "??"],
            ]
        )
        with self.assertRaises(VfsError):
            Vfs.from_csv(path)


if __name__ == "__main__":
    unittest.main()
