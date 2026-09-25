"""Backward-compatible launcher for the modular application.

Prefer `python main.py` for deployment and development.
"""

from main import main


if __name__ == "__main__":
    main()
