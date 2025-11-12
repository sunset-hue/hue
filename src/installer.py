"""Basic package installer, no versioning constraints, no solver yet"""

import requests as r
import json
import zipfile as z
import shutil
import os


def download(pkg: str):
    links = json.loads(
        r.get(
            f"https://pypi.org/simple/{pkg}/",
            headers={"Accept": "application/vnd.pypi.simple.v1+json"},
        ).content
    )
    downloaded = r.get(links["files"][0]["url"])
    with open(f"{pkg}.whl", "wb") as f:
        f.write(downloaded.content)
    zipf = z.ZipFile(f"{pkg}.whl")
    zipf.extractall(pkg)
    try:
        for i in os.listdir(f"{pkg}/{pkg}"):
            shutil.move(f"{pkg}/{pkg}", f"site-packages/{pkg}")
    except:
        pass
    os.removedirs(f"{pkg}")
    os.remove(f"{pkg}.whl")

    # only get first one to download for now


print(download("rich"))
