"""Direct file links — plain streamed HTTP download."""
import os
import re
from urllib.parse import unquote, urlparse

import requests

from .common import USER_AGENT, safe_name


def _filename(resp, url: str) -> str:
    cd = resp.headers.get("content-disposition", "")
    m = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)"?', cd)
    if m:
        return safe_name(unquote(m.group(1)))
    name = os.path.basename(urlparse(url).path) or "download"
    return safe_name(unquote(name))


def run(url: str, workdir: str, job: dict, opts: dict) -> list[str]:
    headers = {"User-Agent": USER_AGENT}
    with requests.get(url, headers=headers, stream=True, timeout=60) as r:
        r.raise_for_status()
        name = _filename(r, url)
        job["title"] = job.get("title") or name
        path = os.path.join(workdir, name)
        total = int(r.headers.get("content-length", 0))
        done = 0
        with open(path, "wb") as f:
            for chunk in r.iter_content(1 << 16):
                f.write(chunk)
                done += len(chunk)
                if total:
                    job["progress"] = int(done / total * 100)
    job["progress"] = 100
    return [path]
