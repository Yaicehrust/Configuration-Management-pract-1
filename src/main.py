"""Application entry point."""

from .app import run_app
from .config import parse_args


def main() -> None:
    """Parse arguments and launch the GUI."""
    run_app(parse_args())


if __name__ == "__main__":
    main()
