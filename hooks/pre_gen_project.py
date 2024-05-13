"""Cookiecutter hook for pre project generation."""

from __future__ import annotations

import re
import sys
from typing import Pattern


# Project names must be letters, numbers, dashes,
# or spaces, but not start with a space or dash.
VALID_PROJECT: Pattern[str] = re.compile(
    r"^([A-Z0-9]|[A-Z0-9][A-Z0-9- ]*[A-Z0-9])$", re.IGNORECASE
)

# PYTHON VERSION SPECIFICATION
# FIXME: do not handle 3.* or 3.8.*
# https://packaging.python.org/en/latest/specifications/version-specifiers/
# https://devguide.python.org/developer-workflow/development-cycle/
# https://iscinumpy.dev/post/bound-version-constraints/#pinning-the-python-version-is-special
VERSION_OPERATORS = r"~=|==|!=|<=|>=|<|>|==="
PYTHON_VERSION = (
    r"(?<version>(?P<release>(?P<major>[0-9]+)(?:(?:\.)(?P<minor>[0-9]+))?"
    r"(?:(?:\.)(?P<micro>[0-9]+))?)(?P<pre>(?:a|b|rc|alpha|beta)(?:[-_\.]?[0-9]+)?)?)"
)
VERSION_PYTHON_SPECIFIER: Pattern[str] = re.compile(
    r"^(~=|==|!=|<=|>=|<|>|===)((([0-9]+)(?:(?:\.)([0-9]+))?(?:(?:\.)([0-9]+))?)((?:a|b|rc|alpha|beta)(?:[-_\.]?[0-9]+)?)?)(,\s*(~=|==|!=|<=|>=|<|>|===)((([0-9]+)(?:(?:\.)([0-9]+))?(?:(?:\.)([0-9]+))?)((?:a|b|rc|alpha|beta)(?:[-_\.]?[0-9]+)?)?))*$"
)


def validate_text(text: str, regex: Pattern[str], error_label: str) -> None:
    """Ensures that `text` is valid.

    Args:
        text: value to check.
        regex: regular expression to check "text" against.
        error_label: text to add to error message if the check fails.

    Raises:
        ValueError: if "text" does not match "regex".
    """
    if regex.fullmatch(text) is None:
        message = f"The project name {text} is not a valid {error_label}"
        raise ValueError(message)


def main() -> None:
    """Calls validation functions."""
    validate_text(
        text="{{ cookiecutter.project_name }}",
        regex=VALID_PROJECT,
        error_label="project name",
    )

    validate_text(
        text="{{ cookiecutter.python }}",
        regex=VERSION_PYTHON_SPECIFIER,
        error_label="python version specifiers",
    )


if __name__ == "__main__":
    sys.exit(main())
