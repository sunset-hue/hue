"""Dependency resolver."""


def resolve_deps(path: str):
    # resolves dependencies using the PKG-INFO of a wheel, since at this stage, we're sure that the package is/has been converted to a wheel.
    