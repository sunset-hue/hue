"""File to manage basic utilities that hue needs."""

import requests as r
import json
import sys
import os
from ._build import build_pkg


def _request_return_url(pkg: str):
    """Gets the download urls for a specific package."""
    return json.loads(
        r.request(
            "GET",
            f"https://pypi.org/simple/{pkg}",
            headers={"Accept": "application/vnd.pypi.simple.v1+json"},
        ).content
    )["files"]


def dist_type(path: str, package: str):
    if f"{package}-" in os.listdir(path):
        return "sdist"
    if f"{package}.dist-info" in os.listdir(path):
        return "whl"


def _correct_idx_for_version():
    # returns the correct index for the type of version number we encounter
    # really repetitive though, need a good way for it to look
    if len(sys.version.split(".")) == 3 and int(sys.version.split(".")[1]) < 10:
        return 4
    if len(sys.version.split(".")) == 3 and int(sys.version.split(".")[1]) >= 10:
        return 5
    if len(sys.version.split(".")) == 2 and int(sys.version.split(".")[1]) < 10:
        return 2
    if len(sys.version.split(".")) == 2 and int(sys.version.split()[1]) >= 10:
        return 3


def get_latest_ver(pkg: str) -> tuple[str, tuple] | None:
    """Gets the latest version of this package's download url if no version number was supplied.
    Note that this only returns the latest version that supports the current python version that the environment is on.
    """
    downloadables: dict = _request_return_url(pkg)
    three_tuple: tuple[int, int, int] = (0, 0, 0)
    success_data: int | None = None
    n = 0
    formatted_sys_ver = (
        sys.version
        if len(sys.version) == 6
        else sys.version + "".join(".0" * (6 - len(sys.version)))
    )
    curr_py_version = formatted_sys_ver[0 : _correct_idx_for_version()]
    for i in downloadables:
        if (
            i.get("requires_python") == None
            or int("".join(curr_py_version.split(".")))
            >= int("".join(i["requires_python"].strip("<=>").split(".")))
            and i["url"].endswith(".whl")
        ):
            to_be_turned = (
                i["filename"]
                .removesuffix(".whl")
                .strip("abcdefghijklmnopqrstuvwxyz-")
                .split(".")
            )
            # since all pypi packages follow semver or some version of that, we can just put it into the 3 tuple, no extra formatting needed
            three_tuple = (to_be_turned[0], to_be_turned[1], to_be_turned[2])
            success_data = n
        n += 1
    if three_tuple == (0, 0, 0):
        print(
            "Error! Could not find downloadable distribution that matches your current python version. Either you can downgrade a python version or specify a compatible package version using ==, >=, <= syntax."
        )
        return
    print(three_tuple)
    return (
        downloadables[success_data]["url"],
        three_tuple,
    )  # pyright: ignore[reportReturnType]


def get_specified_version(ver: str, pkg: str) -> str | None:
    """Gets a specific version of a specific package. Note that NO CHECKS are being run to make sure that this package fits within your current python version."""
    downloadables: dict = _request_return_url(pkg)
    for i in downloadables:
        if i["url"].find(ver):
            return i["url"]


def install(pkg: str, ver: int):
    """Actually does the installing part of installing the package (e.g runs all the stages and also gets dependencies)"""
