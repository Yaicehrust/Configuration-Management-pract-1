"""Graphical user interface for the VFS shell emulator."""

import tkinter as tk

from .shell import Shell


class EmulatorGUI:
    """Display the shell emulator interface."""

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the main application window."""
        self.root = root
        self.shell = Shell()
        self.root.title("VFS")
        self.root.geometry("700x450")
        self._build_widgets()

    def _build_widgets(self) -> None:
        """Create the output and input widgets."""
        self.output = tk.Text(
            self.root,
            state="disabled",
            wrap="word",
        )
        self.output.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(10, 5),
        )

        self.entry = tk.Entry(self.root)
        self.entry.pack(
            fill="x",
            padx=10,
            pady=(5, 10),
        )
        self.entry.bind("<Return>", self._submit)
        self.entry.focus_set()

    def _submit(self, _event: tk.Event) -> None:
        """Process the command entered in the input field."""
        line = self.entry.get()
        self.entry.delete(0, "end")

        if not line.strip():
            return

        self._write(f"> {line}")
        result = self.shell.execute_line(line)

        if result.output:
            self._write(result.output)

        if result.should_exit:
            self.root.destroy()

    def _write(self, text: str) -> None:
        """Append one line to the output area."""
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n")
        self.output.configure(state="disabled")
        self.output.see("end")


def run_app() -> None:
    """Create the application window and start the GUI loop."""
    root = tk.Tk()
    EmulatorGUI(root)
    root.mainloop()
