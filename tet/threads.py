"""Threads posts via Playwright.

Threads loads media through an authenticated, signed GraphQL request whose
doc_id ships in on-demand JS chunks — there is no reliable plain-HTTP path.
So we render the post in headless Chromium, read the media URLs from the DOM,
and fetch the bytes inside the page context (the CDN URLs 403 to bare curl).
"""
import base64
import os
import re

import browser_cookie3
from playwright.sync_api import sync_playwright

from .common import USER_AGENT, safe_name

_COOKIE_DOMAINS = (".threads.com", ".threads.net", ".instagram.com", ".cdninstagram.com")

_FETCH_BYTES = """
async (u) => {
  const r = await fetch(u);
  const b = await r.blob();
  return await new Promise(res => {
    const fr = new FileReader();
    fr.onload = () => res(fr.result.split(',')[1]);
    fr.readAsDataURL(b);
  });
}
"""


def _chrome_cookies() -> list[dict]:
    out = []
    for dom in _COOKIE_DOMAINS:
        try:
            for c in browser_cookie3.chrome(domain_name=dom):
                out.append({
                    "name": c.name, "value": c.value,
                    "domain": c.domain, "path": c.path or "/",
                })
        except Exception:
            pass
    return out


def _author(url: str) -> str:
    m = re.search(r"@([A-Za-z0-9_.]+)", url)
    return m.group(1) if m else "threads"


def run(url: str, workdir: str, job: dict, opts: dict) -> list[str]:
    author = _author(url)
    job["title"] = job.get("title") or f"Threads — @{author}"
    job["uploader"] = f"@{author}"
    job["progress"] = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(user_agent=USER_AGENT)
        cookies = _chrome_cookies()
        if cookies:
            try:
                ctx.add_cookies(cookies)
            except Exception:
                pass
        page = ctx.new_page()
        try:
            page.goto(url, wait_until="networkidle", timeout=45000)
        except Exception:
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(2500)

        videos = page.eval_on_selector_all(
            "video",
            "els => [...new Set(els.map(v => v.currentSrc || v.src).filter(Boolean))]",
        )
        media = [(u, "mp4") for u in videos]

        if not media:  # photo / carousel post — grab the large content images
            imgs = page.eval_on_selector_all(
                "img",
                "els => [...new Set(els.filter(i => i.naturalWidth > 400 && "
                "/cdninstagram|fbcdn/.test(i.src)).map(i => i.src))]",
            )
            media = [(u, "jpg") for u in imgs]

        if not media:
            browser.close()
            raise RuntimeError("No media found on this Threads post")

        job["total"] = len(media)
        paths = []
        for i, (m, ext) in enumerate(media):
            b64 = page.evaluate(_FETCH_BYTES, m)
            data = base64.b64decode(b64)
            name = safe_name(f"{author}_threads_{i + 1}") + f".{ext}"
            path = os.path.join(workdir, name)
            with open(path, "wb") as f:
                f.write(data)
            paths.append(path)
            job["progress"] = int((i + 1) / len(media) * 100)
        browser.close()

    job["thumbnail"] = None
    return paths
