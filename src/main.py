"""Application entry point."""

from .app import run_app
from .config import parse_args


def main() -> None:
    """Parse startup parameters and launch the GUI."""
    config = parse_args()
    run_app(config)


if __name__ == "__main__":
    main()
