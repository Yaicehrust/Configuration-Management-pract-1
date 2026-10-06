"""Graphical user interface for the VFS shell emulator."""

import tkinter as tk

from .config import AppConfig
from .script_runner import run_script
from .shell import Shell
from .vfs import Vfs, VfsError


class EmulatorGUI:
    """Display and control the shell emulator window."""

    def __init__(self, root: tk.Tk, config: AppConfig) -> None:
        """Initialize the window and shell state."""
        self.root = root
        self.config = config
        self.shell = Shell()
        self.root.title("VFS")
        self.root.geometry("760x500")
        self._build_widgets()
        self._print_config()
        self._load_initial_vfs()

    def _build_widgets(self) -> None:
        """Create output and input widgets."""
        self.output = tk.Text(self.root, state="disabled", wrap="word")
        self.output.pack(fill="both", expand=True, padx=10, pady=(10, 5))
        self.entry = tk.Entry(self.root)
        self.entry.pack(fill="x", padx=10, pady=(5, 10))
        self.entry.bind("<Return>", self._submit)
        self.entry.focus_set()

    def _print_config(self) -> None:
        """Display configured startup parameters."""
        self._write(f"VFS path: {self.config.vfs_path or '<не задан>'}")
        self._write(
            f"Script path: {self.config.script_path or '<не задан>'}"
        )

    def _load_initial_vfs(self) -> None:
        """Load the configured startup VFS, when present."""
        if not self.config.vfs_path:
            return
        try:
            self.shell.vfs = Vfs.from_csv(self.config.vfs_path)
            self.shell.current = self.shell.vfs.root
            self._update_title()
            self._write(f"VFS загружена: {self.shell.vfs.name}")
        except VfsError as exc:
            self._write(f"Ошибка: {exc}")

    def start_script(self) -> None:
        """Execute the configured startup script."""
        if not self.config.script_path:
            return
        try:
            run_script(
                self.config.script_path,
                self._execute_for_script,
                self._write,
            )
        except OSError as exc:
            self._write(f"Ошибка запуска скрипта: {exc}")

    def _execute_for_script(self, line: str) -> tuple[str, bool]:
        """Execute one script command and update the GUI state."""
        result = self.shell.execute_line(line)
        if result.vfs_changed:
            self._update_title()
        return result.output, result.should_exit

    def _submit(self, _event: tk.Event) -> None:
        """Execute the command entered by the user."""
        line = self.entry.get()
        self.entry.delete(0, "end")
        if not line.strip():
            return
        self._write(f"> {line}")
        result = self.shell.execute_line(line)
        if result.output:
            self._write(result.output)
        if result.vfs_changed:
            self._update_title()
        if result.should_exit:
            self.root.destroy()

    def _update_title(self) -> None:
        """Update the window title with the current VFS name."""
        self.root.title(f"VFS - {self.shell.vfs.name}")

    def _write(self, text: str) -> None:
        """Append text to the output area."""
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.configure(state="disabled")
        self.output.see("end")


def run_app(config: AppConfig) -> None:
    """Create the main window and start the Tk event loop."""
    root = tk.Tk()
    app = EmulatorGUI(root, config)
    if config.script_path:
        root.after(100, app.start_script)
    root.mainloop()
