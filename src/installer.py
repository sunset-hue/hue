from ._build import build_pkg
from .util import get_latest_ver, get_specified_version
import requests as r


def install(pkg: str, ver: str | None = None, path: str = ".", dest: str = "."):
    """Actually does the installing part of installing the package (e.g runs all the stages and also gets dependencies)"""
    url = get_specified_version(ver, pkg) if ver else get_latest_ver(pkg)
    url_ver = ".".join(url[1]) if isinstance(url, tuple) else ""
    if ver:
        req = r.get(
            url[0] if isinstance(url, tuple) else url if url is not None else ""
        )  # if something goes wrong, it just makes r.get bug out, rather than being not handled at all
        build_pkg(path, dest, pkg, ver if ver else url_ver)
        # resolve_deps(blah blah blah not implemented yet)
