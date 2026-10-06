"""Tests for shell commands."""

import base64
import csv
import tempfile
import unittest

from src.shell import Shell
from src.vfs import Vfs


class ShellTests(unittest.TestCase):
    """Check command behavior across the project stages."""

    def _make_vfs(self) -> Vfs:
        """Create a small in-memory test VFS."""
        handle = tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            suffix=".csv",
            delete=False,
        )
        with handle:
            writer = csv.writer(handle)
            writer.writerow(Vfs.HEADER)
            writer.writerows(
                [
                    ["/", "dir", "0", "root", ""],
                    ["/home", "dir", "0", "root", ""],
                    ["/home/user", "dir", "0", "user", ""],
                    [
                        "/home/user/note.txt",
                        "file",
                        "5",
                        "user",
                        base64.b64encode(b"hello").decode("ascii"),
                    ],
                ]
            )
        return Vfs.from_csv(handle.name)

    def setUp(self) -> None:
        """Create a shell before each test."""
        self.shell = Shell(self._make_vfs())

    def test_ls(self) -> None:
        """List current directory children."""
        result = self.shell.execute_line("ls")
        self.assertIn("home", result.output)

    def test_cd(self) -> None:
        """Change the current virtual directory."""
        result = self.shell.execute_line("cd home")
        self.assertEqual(result.output, "")
        self.assertEqual(self.shell.vfs.path_of(self.shell.current), "/home")

    def test_cd_parent(self) -> None:
        """Resolve parent navigation."""
        self.shell.execute_line("cd /home/user")
        self.shell.execute_line("cd ..")
        self.assertEqual(self.shell.vfs.path_of(self.shell.current), "/home")

    def test_du(self) -> None:
        """Calculate a directory size."""
        result = self.shell.execute_line("du -s /home")
        self.assertIn("5", result.output)

    def test_cal(self) -> None:
        """Generate a requested month calendar."""
        result = self.shell.execute_line("cal 10 2026")
        self.assertIn("October", result.output)

    def test_chown_memory_only(self) -> None:
        """Change owner without writing back to disk."""
        result = self.shell.execute_line("chown admin /home/user/note.txt")
        self.assertIn("admin", result.output)
        node = self.shell.vfs.resolve("/home/user/note.txt")
        self.assertEqual(node.owner, "admin")

    def test_vfs_load(self) -> None:
        """Load another VFS and reset the current directory."""
        handle = tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", suffix=".csv", delete=False
        )
        with handle:
            writer = csv.writer(handle)
            writer.writerow(Vfs.HEADER)
            writer.writerow(["/", "dir", "0", "root", ""])
            writer.writerow(["/new", "dir", "0", "root", ""])
        result = self.shell.execute_line(f"vfs-load {handle.name}")
        self.assertTrue(result.vfs_changed)
        self.assertEqual(self.shell.vfs.path_of(self.shell.current), "/")
        self.assertIn("new", self.shell.execute_line("ls").output)

    def test_errors(self) -> None:
        """Report unknown commands and invalid arguments."""
        self.assertIn(
            "неизвестная команда",
            self.shell.execute_line("xxx").output,
        )
        self.assertIn("Использование", self.shell.execute_line("cd a b").output)
        self.assertIn(
            "Каталог не найден",
            self.shell.execute_line("cd /none").output,
        )
        self.assertIn(
            "Использование",
            self.shell.execute_line("vfs-load").output,
        )


    def test_chown_recursive(self) -> None:
        """Change owners recursively in memory."""
        result = self.shell.execute_line(
            "chown -R admin /home/user"
        )
        self.assertIn("admin", result.output)
        node = self.shell.vfs.resolve("/home/user/note.txt")
        self.assertEqual(node.owner, "admin")

    def test_vfs_load_errors(self) -> None:
        """Report missing and malformed VFS files."""
        missing = self.shell.execute_line("vfs-load data/vfs/missing.csv")
        invalid = self.shell.execute_line("vfs-load data/vfs/invalid.csv")
        self.assertIn("не найден", missing.output)
        self.assertIn("base64", invalid.output)

    def test_exit(self) -> None:
        """Request application termination."""
        result = self.shell.execute_line("exit")
        self.assertTrue(result.should_exit)


if __name__ == "__main__":
    unittest.main()
