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
        self.root.minsize(600, 400)

        self._build_widgets()
        self._print_config()
        self._load_initial_vfs()

        def _build_widgets(self) -> None:
            """Create and arrange the terminal widgets."""
            self.root.configure(bg="#111111")
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_rowconfigure(1, weight=0)
            self.root.grid_columnconfigure(0, weight=1)
            self._build_output()
            self._build_input()

        def _build_output(self) -> None:
            """Create the terminal output area and scrollbar."""
            self.terminal_frame = tk.Frame(self.root, bg="#111111")
            self.terminal_frame.grid(
               row=0, column=0, sticky="nsew", padx=10, pady=(10, 5)
            )
            self.terminal_frame.grid_rowconfigure(0, weight=1)
            self.terminal_frame.grid_columnconfigure(0, weight=1)
            self._build_output_text()
            self._build_scrollbar()

        def _build_output_text(self) -> None:
            """Create the scrollable terminal text area."""
            self.output = tk.Text(
               self.terminal_frame,
               state="disabled",
               wrap="word",
               bg="#111111",
                fg="#e6e6e6",
                insertbackground="#e6e6e6",
                selectbackground="#333333",
                selectforeground="#ffffff",
                font=("Consolas", 11),
                relief="flat",
                borderwidth=0,
            )
            self.output.grid(row=0, column=0, sticky="nsew")

        def _build_scrollbar(self) -> None:
            """Attach a scrollbar to the terminal output area."""
            scrollbar = tk.Scrollbar(
                self.terminal_frame,
                command=self.output.yview,
                bg="#222222",
                troughcolor="#111111",
                activebackground="#444444",
            )
            scrollbar.grid(row=0, column=1, sticky="ns")
            self.output.configure(yscrollcommand=scrollbar.set)

        def _build_input(self) -> None:
            """Create the command prompt and input field."""
            self.input_frame = tk.Frame(self.root, bg="#111111")
            self.input_frame.grid(
                row=1, column=0, sticky="ew", padx=10, pady=(5, 10)
            )
            self.input_frame.grid_columnconfigure(1, weight=1)
            self._build_prompt()
            self._build_entry()

        def _build_prompt(self) -> None:
            """Create the terminal prompt symbol."""
            prompt = tk.Label(
                self.input_frame,
                text=">",
                bg="#111111",
                fg="#e6e6e6",
                font=("Consolas", 11),
            )
            prompt.grid(row=0, column=0, padx=(4, 8))

        def _build_entry(self) -> None:
            """Create and configure the command input field."""
            self.entry = tk.Entry(
                self.input_frame,
                bg="#1b1b1b",
                fg="#e6e6e6",
                insertbackground="#e6e6e6",
                selectbackground="#333333",
                selectforeground="#ffffff",
                font=("Consolas", 11),
                relief="flat",
            )
            self.entry.grid(row=0, column=1, sticky="ew", ipady=6)
            self.entry.bind("<Return>", self._submit)
            self.entry.focus_set()

        def _print_config(self) -> None:
            """Display configured startup parameters."""
            self._write(
                f"VFS path: {self.config.vfs_path or '<не задан>'}"
            )
            self._write(
                f"Script path: {self.config.script_path or '<не задан>'}"
            )

    def _load_initial_vfs(self) -> None:
        """Load the configured startup VFS, when present."""
        if not self.config.vfs_path:
            return

        try:
            self.shell.vfs = Vfs.from_csv(
                self.config.vfs_path
            )
            self.shell.current = self.shell.vfs.root
            self._update_title()
            self._write(
                f"VFS загружена: {self.shell.vfs.name}"
            )
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
            self._write(
                f"Ошибка запуска скрипта: {exc}"
            )

    def _execute_for_script(
        self,
        line: str,
    ) -> tuple[str, bool]:
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
        self.root.title(
            f"VFS - {self.shell.vfs.name}"
        )

    def _write(self, text: str) -> None:
        """Append text to the output area."""
        self.output.configure(state="normal")
        self.output.insert(
            "end",
            text + "\n",
        )
        self.output.configure(state="disabled")
        self.output.see("end")


def run_app(config: AppConfig) -> None:
    """Create the main window and start the Tk event loop."""
    root = tk.Tk()
    app = EmulatorGUI(root, config)

    if config.script_path:
        root.after(
            100,
            app.start_script,
        )

    root.mainloop()