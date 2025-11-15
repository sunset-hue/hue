"""Contains the necessary functions needed to build a sdist or wheel."""

import tomllib
import subprocess
import setuptools.build_meta as build
import os


def _wheel_to_dict(path: str):
    # just parses the stuff in WHEEL, will need this to extend to METADATA later
    parsed = {}
    for i in os.listdir(f"{path}.dist-info/WHEEL"):
        parsed[i.split(":")[0]] = i.split(":")[1]
    return parsed


def metadata_to_dict(path: str):
    parsed = {}
    for i in os.listdir(f"{path}.dist-info/METADATA"):
        parsed[i.split(":")[0]] = i.split(":")[1]
    return parsed


def type_and_system(path: str) -> list[str]:
    tup_return = []
    if len(os.listdir(path)) == 1:
        tup_return[0] = "sdist"
    else:
        tup_return[0] = "whl"
    if tup_return[0] == "whl":
        setup_tools = _wheel_to_dict(path)
        tup_return[1] = setup_tools["Generator"]
        return tup_return
    else:
        toml = tomllib.load(open(f"{path}/pyproject.toml", "rb"))
        tup_return[1] = toml["requires"][0]
        return tup_return
