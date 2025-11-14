"""Contains the dependency resolver."""

import tomllib
from typing import BinaryIO


def resolve_deps_sdist(path: str):
    setup_system = tomllib.load(open(f"{path}/pyproject.toml", "rb"))["build-system"][
        "requires"
    ][0]
    # what is this ugliness that black formatter has created
