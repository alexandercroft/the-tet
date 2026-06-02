"""Public Telegram channel media via the t.me embed page."""
import os
import re

import requests

from .common import USER_AGENT, safe_name


def _media_urls(html: str) -> list[tuple[str, str]]:
    vids = set(re.findall(r'<video[^>]+src="([^"]+)"', html))
    vids |= set(re.findall(r'"(https://[^"]+\.mp4[^"]*)"', html))
    photos = set(re.findall(r"background-image:url\('([^']+)'\)", html))
    photos = {p for p in photos if "telesco" in p or "cdn" in p}
    return [(u, "mp4") for u in vids] + [(u, "jpg") for u in photos]


def run(url: str, workdir: str, job: dict, opts: dict) -> list[str]:
    m = re.search(r"t\.me/(?:s/)?([^/?#]+)/(\d+)", url)
    slug = f"{m.group(1)}_{m.group(2)}" if m else "telegram"
    job["title"] = job.get("title") or f"Telegram — {slug}"
    job["progress"] = None

    embed = url.split("?")[0] + "?embed=1&mode=tme"
    headers = {"User-Agent": USER_AGENT}
    html = requests.get(embed, headers=headers, timeout=20).text
    media = _media_urls(html)
    if not media:
        raise RuntimeError("No media found on this Telegram post (private or text-only?)")

    job["total"] = len(media)
    paths = []
    for i, (u, ext) in enumerate(media):
        name = safe_name(f"{slug}_{i + 1}") + f".{ext}"
        path = os.path.join(workdir, name)
        with requests.get(u, headers=headers, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(path, "wb") as f:
                for chunk in r.iter_content(1 << 16):
                    f.write(chunk)
        paths.append(path)
        job["progress"] = int((i + 1) / len(media) * 100)
    return paths
