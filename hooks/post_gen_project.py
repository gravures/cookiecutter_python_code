"""Cookiecutter hook for pre project generation."""

from __future__ import annotations

import sys
from pathlib import Path


def main():
    """Make empty directories."""
    (Path.cwd() / "src").mkdir(exist_ok=True)
    (Path.cwd() / "typings").mkdir(exist_ok=True)


if __name__ == "__main__":
    sys.exit(main())
