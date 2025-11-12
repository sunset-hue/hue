"""Basic package installer, no versioning constraints, no solver yet"""

import requests as r
import json
import zipfile as z


def download(pkg: str):
    links = json.loads(
        r.get(
            f"https://pypi.org/simple/{pkg}/",
            headers={"Accept": "application/vnd.pypi.simple.v1+json"},
        ).content
    )
    downloaded = r.get(links["files"][0]["url"])
    print(links["files"][0])
    with open(f"first_things_first.whl", "wb") as f:
        f.write(downloaded.content)
    # only get first one to download for now


print(download("discmoji"))
