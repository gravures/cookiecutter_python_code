"""Local Jinja2 extensions module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generator, Literal, TypeAlias

from jinja2.ext import Extension
from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import Version


if TYPE_CHECKING:
    from jinja2.environment import Environment


SUPPORTED_VERSIONS = {
    3: {
        8: range(19),
        9: range(19),
        10: range(14),
        11: range(9),
        12: range(3),
    }
}

Schemes: TypeAlias = Literal["major", "minor", "micro"]


def python_versions(precision: Schemes) -> Generator[Version, None, None]:
    """Yiel supported minor Python versions."""
    for major in SUPPORTED_VERSIONS:
        if precision == "major":
            yield Version(f"{major}")
        else:
            for minor in SUPPORTED_VERSIONS[major]:
                if precision == "minor":
                    yield Version(f"{major}.{minor}")
                else:
                    for micro in SUPPORTED_VERSIONS[major][minor]:
                        yield Version(f"{major}.{minor}.{micro}")


def create_specifier_set(value: str) -> SpecifierSet | None:
    """Create a SpecifierSet and handle InvalidSpecifier exception."""
    try:
        return SpecifierSet(specifiers=value)
    except InvalidSpecifier:
        return None


class PythonVersionExtension(Extension):
    """Jinja2 extension."""

    def __init__(self, environment: Environment) -> None:
        """Initialize the extension with the given environment."""
        super().__init__(environment)

        def py_vers_tox(value: str) -> str:
            """Formats the SpecifierSet string <value> for use in tox.ini."""
            sp = create_specifier_set(value)
            if sp is None:
                return ""
            versions = list(sp.filter(python_versions("minor")))
            versions = [str(v.minor) for v in versions]
            return "py3{" + ",".join(versions) + "}"

        def py_vers_yaml(value: str) -> str:
            """Formats the SpecifierSet string <value> as a YAML list for use in gh actions."""
            sp = create_specifier_set(value)
            if sp is None:
                return ""
            versions: list[str] = list(map(str, list(sp.filter(python_versions("minor")))))
            return str(versions)

        def py_vers_minimal(value: str, precision: Schemes) -> str:
            """Returns the minimal supported Python version."""
            sp = create_specifier_set(value)
            if sp is None:
                return ""
            supported = list(sp.filter(python_versions(precision=precision)))
            version = min(supported)
            return str(version)

        environment.filters["py_vers_tox"] = py_vers_tox
        environment.filters["py_vers_yaml"] = py_vers_yaml
        environment.filters["py_vers_minimal"] = py_vers_minimal  # pyright:ignore[reportArgumentType]
