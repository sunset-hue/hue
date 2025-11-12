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


def get_latest_ver(pkg: Package):
    downloadables: dict = _request_return_url(pkg)
    three_tuple: tuple[int, int, int] = (0, 0, 0)
    curr_py_version = sys.version[
        0:2
    ]  # for example it would show us up to 3.13 if the current version was 3.13.5
    # for caching versions so we can tell which one's the newest
    for i in downloadables:
        if i["requires_python"] == None or int(
            "".join(curr_py_version.split("."))
        ) >= int("".join(i["requires_python"].strip("<=>").split("."))):
            # here, my thought process is to just strip all the dots and turn the first 2 numbers into a integer, so we can compare those 2 values (this might cause a problem with packages that require more precision with versioning though, but we'll handle that later)
            to_be_turned = i["filename"].strip("abcdefghijklmnopqrstuvwxyz").split(".")
            # first few results here (if package name isn't alpha numeric is the version numbers we need)
            # since all pypi packages follow semver or some version of that, we can just put it into the 3 tuple, no extra formatting needed
            three_tuple = (to_be_turned[0], to_be_turned[1], to_be_turned[2])
    if three_tuple == (0, 0, 0):
        print(
            "Error! Could not find downloadable distribution that matches your current python version. Either you can downgrade or specify a version using ==, >=, <= syntax."
        )
