"""Cookiecutter hook for pre project generation."""

from __future__ import annotations

import re
import sys
from typing import Pattern

# A valid name consists only of ASCII letters 
# and numbers, period, underscore and hyphen. 
# It must start and end with a letter or number.
# https://packaging.python.org/en/latest/specifications/name-normalization/ 
VALID_PROJECT_NAME: Pattern[str] = re.compile(
    r"^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$", re.IGNORECASE
)


# Repository names must be lower-case letters,
# numbers, or underscores, but not start with an underscore.
VALID_REPO_NAME: Pattern[str] = re.compile(r"^([a-z0-9]|[a-z0-9][a-z0-9_]*[a-z0-9])$")


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
VALID_PYTHON_VERSION_SPECIFIER: Pattern[str] = re.compile(
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
    if not text or regex.fullmatch(text) is None:
        message = f"Input <{text}> is not a valid {error_label}"
        raise ValueError(message)


def main() -> None:
    """Calls validation functions."""
    validate_text(
        text="{{ cookiecutter.project_name }}",
        regex=VALID_PROJECT_NAME,
        error_label="project name",
    )

    validate_text(
        text="{{ cookiecutter.repo_name }}",
        regex=VALID_REPO_NAME,
        error_label="repository name",
    )

    validate_text(
        text="{{ cookiecutter.python }}",
        regex=VALID_PYTHON_VERSION_SPECIFIER,
        error_label="python version specifiers set",
    )


if __name__ == "__main__":
    sys.exit(main())
