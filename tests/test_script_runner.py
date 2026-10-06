"""Tests for startup script execution."""

import tempfile
import unittest
from pathlib import Path

from src.script_runner import run_script


class ScriptRunnerTests(unittest.TestCase):
    """Check comments, input display and command output."""

    def test_comments_are_skipped(self) -> None:
        """Ignore empty and commented lines."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "start.txt"
            path.write_text(
                "# comment\n\nls\ncd test\n",
                encoding="utf-8",
            )
            shown: list[str] = []
            run_script(
                str(path),
                lambda line: (f"ok: {line}", False),
                shown.append,
            )
        self.assertEqual(
            shown,
            ["> ls", "ok: ls", "> cd test", "ok: cd test"],
        )

    def test_script_stops_after_exit(self) -> None:
        """Stop processing when the command asks the shell to exit."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "start.txt"
            path.write_text("ls\nexit\nls\n", encoding="utf-8")
            shown: list[str] = []
            run_script(
                str(path),
                lambda line: ("", line == "exit"),
                shown.append,
            )
        self.assertEqual(shown, ["> ls", "> exit"])


if __name__ == "__main__":
    unittest.main()
