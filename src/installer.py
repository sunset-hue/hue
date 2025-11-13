"""Basic package installer"""

import requests as r
from _inbuilt_types.pkgs import Package
import os
import json
import sys
import typing


# reworking everything to look cleaner


def _request_return_url(pkg: Package):
    return json.loads(
        r.request(
            "GET",
            f"https://pypi.org/simple/{pkg.pkg_name}",
            headers={"Accept": "application/vnd.pypi.simple.v1+json"},
        ).content
    )["files"]


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


def get_latest_ver(pkg: Package) -> str | None:
    """Gets the latest version of this package's download url if no version number was supplied.
    Note that this only returns the latest version that supports the current python version that `hue`'s installed on.
    """
    downloadables: dict = _request_return_url(pkg)
    three_tuple: tuple[int, int, int] = (0, 0, 0)
    success_data: int | None = None
    n = 0
    curr_py_version = sys.version[0 : _correct_idx_for_version()]
    for i in downloadables:
        if i["requires_python"] == None or int(
            "".join(curr_py_version.split("."))
        ) >= int("".join(i["requires_python"].strip("<=>").split("."))):
            to_be_turned = (
                i["filename"]
                .removesuffix(".tar.gz")
                .strip("abcdefghijklmnopqrstuvwxyz")
                .split(".")
            )
            # first few results here (if package name isn't alpha numeric is the version numbers we need)
            # since all pypi packages follow semver or some version of that, we can just put it into the 3 tuple, no extra formatting needed
            three_tuple = (to_be_turned[0], to_be_turned[1], to_be_turned[2])
            success_data = n
        n += 1
    if three_tuple == (0, 0, 0):
        print(
            "Error! Could not find downloadable distribution that matches your current python version. Either you can downgrade a python version or specify a compatible package version using ==, >=, <= syntax."
        )
        return
    return downloadables[success_data]["url"]


def install_into_site(pkg: Package):
    # since we have no outside interface yet, this'll be enough
    ...
