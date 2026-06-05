"""Instagram reels, posts, carousels & photos.

yt-dlp goes first: it downloads public reels/videos **without any login**, which
is the common case for most users. gallery-dl is the fallback — it's stronger for
multi-image carousels and login-gated content, but needs an Instagram session in
Chrome. This order means a logged-out user still gets public reels/videos.
"""
import os
import subprocess

import yt_dlp

from .common import USER_AGENT, chrome_cli_spec, ydl_cookiesfrombrowser


def _ytdlp(url: str, workdir: str, job: dict, use_cookies: bool) -> list[str]:
    def hook(d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            if total:
                job["progress"] = int(d.get("downloaded_bytes", 0) / total * 100)

    ydl_opts = {
        "outtmpl": os.path.join(workdir, "%(title).70s [%(id)s].%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "http_headers": {"User-Agent": USER_AGENT},
        "progress_hooks": [hook],
        "merge_output_format": "mp4",
    }
    if use_cookies:
        ydl_opts["cookiesfrombrowser"] = ydl_cookiesfrombrowser()

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    files = [os.path.join(workdir, f) for f in os.listdir(workdir)]
    if files and isinstance(info, dict):
        job["title"] = info.get("title") or job.get("title")
        job["uploader"] = info.get("uploader") or info.get("channel")
        job["thumbnail"] = info.get("thumbnail")
    return files


def _gallery_dl(url: str, workdir: str, with_cookies: bool) -> list[str]:
    cmd = ["gallery-dl", "-D", workdir]
    if with_cookies:
        cmd += ["--cookies-from-browser", chrome_cli_spec()]
    cmd.append(url)
    subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    return [os.path.join(workdir, f) for f in os.listdir(workdir)]


def run(url: str, workdir: str, job: dict, opts: dict) -> list[str]:
    job["progress"] = None

    # 1) yt-dlp — public reels/videos work with no login (the common case);
    #    retry with cookies for login-gated content if the first try is empty.
    for use_cookies in (False, True):
        try:
            files = _ytdlp(url, workdir, job, use_cookies)
            if files:
                job["progress"] = 100
                return files
        except Exception:
            pass

    # 2) gallery-dl fallback — best for multi-image carousels / when signed in.
    for with_cookies in (True, False):
        files = _gallery_dl(url, workdir, with_cookies)
        if files:
            job["progress"] = 100
            return files

    raise RuntimeError(
        "Instagram: could not download — the post may be private or login-gated "
        "(sign into Instagram in Chrome to enable gallery-dl fallback)."
    )
