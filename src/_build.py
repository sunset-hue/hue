"""Contains the necessary functions needed to build a sdist or wheel."""

import tomllib
import setuptools.build_meta as tools_build
import flit.buildapi as flit_build
import hatchling.build as hatch_build
import poetry.masonry.api as poetry_build
import shutil
import zipfile
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


def build_pkg(path: str, dest: str, pkg: str, ver: str):
    """Converts a sdist into wheel format if needed, else just unzips the wheel."""
    system = {
        "setuptools": tools_build,
        "flit": flit_build,
        "hatchling": hatch_build,
        "poetry": poetry_build,
    }
    type_and_sys = type_and_system(path)
    if type_and_sys[0] == "whl":
        # just a simple unpack
        unzipped = zipfile.ZipFile(path)
        unzipped.extractall(dest)
    else:
        for i in os.listdir(f"{path}/{pkg}-{ver}/"):
            if i.endswith(".egg-info"):
                continue  # this is setuptools specific, may change
            shutil.move(f"{path}/{pkg}-{ver}/{pkg}/{i}", f"{path}/{pkg}/")
            # moves everything from the sdist to a new directory that conforms to the structure of a wheel
            shutil.rmtree(f"{path}/{pkg}-{ver}")
            # deletes the old sdist we had earlier, which is empty except for non py files/folders
        for i in system.keys():
            if i in type_and_sys[0]:
                system[i].build_wheel(path, dest)
                # metadatadirectory for these is blank
                # not type annotated properly (on vscode) but since all of these build backends conform to pep 517 we're safe here
            else:
                raise ValueError(
                    "build_system is not a recognized build system. Please check your pyproject.toml."
                )
        build_pkg(path, dest, pkg, ver)
        # we can just recurse because ofc, the former sdist has been converted into a wheel and can be unzipped
