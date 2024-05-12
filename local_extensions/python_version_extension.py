"""Local Jinja2 extensions module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from jinja2.ext import Extension
from packaging.specifiers import InvalidSpecifier, SpecifierSet


if TYPE_CHECKING:
    from jinja2.environment import Environment

MINOR_VERSIONS: list[str] = ["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"]


class PythonVersionExtension(Extension):
    """Jinja2 extension."""

    def __init__(self, environment: Environment) -> None:
        """Initialize the extension with the given environment."""
        super().__init__(environment)

        def py_vers_tox(value: str) -> str:
            """Return a string for tox.ini."""
            try:
                sp: SpecifierSet = SpecifierSet(specifiers=value)
            except InvalidSpecifier:
                return ""
            else:
                versions = list(sp.filter(MINOR_VERSIONS))
                versions = [v.lstrip("3.") for v in versions]
                return "py3{" + ",".join(versions) + "}"

        def py_vers_yaml(value: str) -> str:
            """Return a string as a YAML list."""
            try:
                sp: SpecifierSet = SpecifierSet(specifiers=value)
            except InvalidSpecifier:
                return ""
            else:
                versions = list(sp.filter(MINOR_VERSIONS))
                return str(versions)

        environment.filters["py_vers_tox"] = py_vers_tox
        environment.filters["py_vers_yaml"] = py_vers_yaml
