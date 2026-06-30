"""Threads posts — exact media via SSR-JSON.

The linked post's media (image_versions2 / video_versions) is embedded in the
page's initial JSON, bound to the post's shortcode. We fetch with Chrome cookies,
parse that JSON, and download EXACTLY that post's media. This fixes the old
headless-DOM scrape that grabbed every large <img> on the rendered page —
including neighbouring feed/recommended posts (1 photo -> 5 files, wrong media).

Requirements: Chrome logged into Threads (cookies for .threads.com) and the
`Accept: text/html` header — without it Threads serves a lighter variant with no
SSR thread JSON.

If the deterministic path comes up empty, an optional `threads_fallback` module
(if present) gets a chance to fetch the media; absent that, we raise cleanly.
"""
import json
import os
import re
import sys
from html.parser import HTMLParser

import browser_cookie3
import requests

from .common import USER_AGENT, safe_name


def _author(url: str) -> str:
    m = re.search(r"@([A-Za-z0-9_.]+)", url)
    return m.group(1) if m else "threads"


def _shortcode(url: str) -> str | None:
    m = re.search(r"/post/([A-Za-z0-9_-]+)", url)
    return m.group(1) if m else None


def _session() -> requests.Session:
    s = requests.Session()
    # Only Threads cookies authenticate the page. Merging instagram/cdn cookies by
    # name would clobber the threads `sessionid` with the instagram one and we'd get
    # the truncated anonymous page (0 thread_items). threads.com wins (setdefault).
    jar = {}
    for dom in (".threads.com", ".threads.net"):
        try:
            for c in browser_cookie3.chrome(domain_name=dom):
                jar.setdefault(c.name, c.value)
        except Exception:
            pass
    s.cookies.update(jar)  # host-agnostic: same trick lets the signed CDN fetch succeed
    s.headers.update({
        "User-Agent": USER_AGENT,
        # Accept: text/html is REQUIRED — with the default */* Threads serves a
        # lighter variant without the SSR thread JSON (0 thread_items).
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en,ru;q=0.9",
        "Sec-Fetch-Site": "same-origin",
    })
    return s


# ── SSR-JSON parsing (media bound to the post, not the DOM) ───────────────────

class _JSONScripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts = []
        self._attrs = None
        self._buf = None

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self._attrs = dict(attrs)
            self._buf = []

    def handle_data(self, data):
        if self._buf is not None:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._buf is not None:
            self.scripts.append((self._attrs or {}, "".join(self._buf)))
            self._attrs = None
            self._buf = None


def _json_blobs(page: str):
    parser = _JSONScripts()
    parser.feed(page)
    for attrs, body in parser.scripts:
        if attrs.get("type") == "application/json" and body.lstrip().startswith("{"):
            try:
                yield json.loads(body)
            except Exception:
                continue


def _walk(obj):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from _walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk(v)


def _find_post(page: str, shortcode: str | None) -> dict | None:
    """The exact post node: matched by shortcode, else the first thread post."""
    first = None
    for blob in _json_blobs(page):
        for node in _walk(blob):
            for item in node.get("thread_items") or []:
                post = item.get("post") or {}
                if not post:
                    continue
                if first is None:
                    first = post
                if shortcode and post.get("code") == shortcode:
                    return post
    return first


def _pick_image(node: dict) -> str | None:
    cands = [c for c in ((node.get("image_versions2") or {}).get("candidates") or []) if c.get("url")]
    if not cands:
        return None
    return max(cands, key=lambda c: (c.get("width") or 0) * (c.get("height") or 0))["url"]


def _pick_video(node: dict) -> str | None:
    vers = [v for v in (node.get("video_versions") or []) if v.get("url")]
    if not vers:
        return None
    return max(vers, key=lambda v: (v.get("width") or 0) * (v.get("height") or 0))["url"]


def _ext_from_url(url: str, default: str) -> str:
    m = re.search(r"\.(jpg|jpeg|png|webp|mp4|mov|webm)(?:\?|$)", url, re.I)
    return m.group(1).lower() if m else default


def _media_source(post: dict) -> dict:
    """The node that actually carries the media.

    A text post with an attached photo/video/carousel keeps it under
    text_post_app_info.linked_inline_media — a nested post node — rather than on
    the post node itself. So if this post carries no media of its own, drop into
    the inline-media node before giving up.
    """
    if post.get("carousel_media") or _pick_image(post) or _pick_video(post):
        return post
    inline = (post.get("text_post_app_info") or {}).get("linked_inline_media")
    return inline or post


def _post_media(post: dict) -> list[tuple[str, str]]:
    """(url, ext) for EXACTLY this post — single or carousel, one file per item."""
    post = _media_source(post)
    items = post.get("carousel_media") or [post]
    media = []
    for it in items:
        v = _pick_video(it)
        if v:
            media.append((v, _ext_from_url(v, "mp4")))
            continue
        img = _pick_image(it)
        if img:
            media.append((img, _ext_from_url(img, "jpg")))
    return media


# ── Downloads ─────────────────────────────────────────────────────────────────

def _download(session: requests.Session, media: list, workdir: str, author: str, job: dict) -> list[str]:
    paths = []
    try:
        for i, (url, ext) in enumerate(media, 1):
            r = session.get(url, timeout=30, headers={"Referer": "https://www.threads.com/"})
            r.raise_for_status()
            name = safe_name(f"{author}_threads_{i}") + f".{ext}"
            path = os.path.join(workdir, name)
            with open(path, "wb") as f:
                f.write(r.content)
            paths.append(path)
            job["progress"] = int(i / len(media) * 100)
    except Exception:
        for p in paths:  # don't leave a partial set behind for the fallback to mix with
            try:
                os.remove(p)
            except OSError:
                pass
        raise
    return paths


def _optional_fallback(url: str, shortcode: str | None, workdir: str, job: dict) -> list[str]:
    """Pluggable local-only fallback. No-op if the optional module isn't installed."""
    try:
        from .threads_fallback import fetch as fallback_fetch
    except Exception:
        return []
    try:
        return fallback_fetch(url, shortcode, workdir, job)
    except Exception as e:
        print(f"[the-tet] threads: fallback failed: {e}", file=sys.stderr)
        return []


def run(url: str, workdir: str, job: dict, opts: dict) -> list[str]:
    author = _author(url)
    shortcode = _shortcode(url)
    job["title"] = job.get("title") or f"Threads — @{author}"
    job["uploader"] = f"@{author}"
    job["progress"] = None

    session = _session()

    # deterministic: media bound to the post's pk
    media = []
    try:
        page = session.get(url, timeout=30).text
        post = _find_post(page, shortcode)
        if post:
            media = _post_media(post)
    except Exception as e:
        print(f"[the-tet] threads: SSR fetch/parse failed: {e}", file=sys.stderr)

    paths = []
    if media:
        job["total"] = len(media)
        try:
            paths = _download(session, media, workdir, author, job)
        except Exception as e:
            print(f"[the-tet] threads: download failed ({e})", file=sys.stderr)

    # optional fallback (local-only; absent in the public repo)
    if not paths:
        paths = _optional_fallback(url, shortcode, workdir, job)

    if not paths:
        raise RuntimeError("No media found on this Threads post")

    job["thumbnail"] = None
    return paths
