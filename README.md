# The TET

**Universal media extractor** with a light tactical-HUD interface. Paste a link —
YouTube, Instagram, Threads, a public Telegram post, or a direct file — and it
downloads straight into your folder. Self-hosted, runs locally.

![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## What it handles

| Source | Engine | Notes |
|--------|--------|-------|
| **Video** — YouTube, TikTok, X/Twitter, Vimeo, Reddit, IG Reels, 1000+ sites | [yt-dlp](https://github.com/yt-dlp/yt-dlp) | MP4, best quality |
| **Instagram** — posts, carousels, photos, reels | [gallery-dl](https://github.com/mikf/gallery-dl) | needs an Instagram login in Chrome |
| **Threads** — videos & images | headless Chromium ([Playwright](https://playwright.dev/python/)) | renders the post, grabs media from the DOM |
| **Telegram** — public channel posts | built-in `t.me` embed scraper | videos + photos |
| **Direct files** — mp4, pdf, zip, jpg… | streamed HTTP download | |

The source is auto-detected from the URL and routed to the right engine.
Files land directly in your output folder (default `~/Downloads`).

## Quick start

```bash
brew install python ffmpeg          # system prerequisites
git clone https://github.com/<you>/the-tet.git
cd the-tet
./run.sh                            # sets up venv, installs deps + Chromium
```

Open **http://127.0.0.1:8900**, paste a link, hit **EXTRACT**.

The first run creates a virtualenv, installs the Python deps from
`requirements.txt`, and downloads a Chromium build for Playwright (~150 MB, used
only for Threads).

## Configuration

Environment variables:

| Variable | Default | Purpose |
|----------|---------|---------|
| `TET_OUTPUT` | `~/Downloads` | where downloads are saved |
| `TET_CHROME_PROFILE` | *(default profile)* | Chrome profile to read cookies from, e.g. `"Default"` or `"Profile 1"` |
| `PORT` | `8900` | server port |

```bash
TET_OUTPUT=~/Movies/TET TET_CHROME_PROFILE="Default" ./run.sh
```

## Cookies & logins

Instagram (and private/age-gated video) needs an authenticated session. The TET
reads cookies from your local **Chrome**. Make sure you're logged into the
relevant site in Chrome; if your session lives in a non-default Chrome profile,
point `TET_CHROME_PROFILE` at it.

## Stack

- **Backend:** Python + Flask, one small module per engine (`tet/`)
- **Frontend:** vanilla HTML/CSS/JS, no build step
- **Engines:** yt-dlp · gallery-dl · Playwright · requests

## Disclaimer

For personal use only. Respect copyright and the terms of service of the
platforms you download from.

## License

[MIT](LICENSE)
