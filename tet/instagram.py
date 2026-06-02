"""Instagram posts, carousels, photos and reels via gallery-dl."""
import os
import subprocess

from .common import chrome_cli_spec


def run(url: str, workdir: str, job: dict, opts: dict) -> list[str]:
    job["progress"] = None  # gallery-dl gives no clean overall %, animate instead
    cmd = [
        "gallery-dl", "-D", workdir,
        "--cookies-from-browser", chrome_cli_spec(),
        url,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    files = [os.path.join(workdir, f) for f in os.listdir(workdir)]
    if not files:
        # Retry without cookies (public content) before giving up.
        proc = subprocess.run(
            ["gallery-dl", "-D", workdir, url],
            capture_output=True, text=True, timeout=600,
        )
        files = [os.path.join(workdir, f) for f in os.listdir(workdir)]
    if not files:
        err = (proc.stderr or proc.stdout or "gallery-dl produced no files").strip()
        raise RuntimeError(err.splitlines()[-1] if err else "gallery-dl failed")
    job["progress"] = 100
    return files
