"""Shared helpers: output dir, filename safety, browser cookies, file moves."""
import os
import re
import shutil

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

OUTPUT_DIR = os.path.expanduser(os.environ.get("TET_OUTPUT", "~/Downloads"))

# Optional Chrome profile for cookie extraction (e.g. "Default", "Profile 1").
# Instagram needs an active login; if your session lives in a non-default
# profile, set TET_CHROME_PROFILE to point cookie extraction at it.
CHROME_PROFILE = os.environ.get("TET_CHROME_PROFILE") or None


def chrome_cli_spec() -> str:
    """Browser spec string for yt-dlp / gallery-dl --cookies-from-browser."""
    return f"chrome:{CHROME_PROFILE}" if CHROME_PROFILE else "chrome"


def ydl_cookiesfrombrowser() -> tuple:
    """(browser, profile, keyring, container) tuple for yt-dlp."""
    return ("chrome", CHROME_PROFILE, None, None) if CHROME_PROFILE else ("chrome",)


def safe_name(name: str, maxlen: int = 90) -> str:
    name = re.sub(r'[\\/:*?"<>|\n\r\t]', "", name or "").strip()
    return (name[:maxlen].strip() or "tet_download")


def unique_path(directory: str, filename: str) -> str:
    """Return a path in `directory` for `filename`, avoiding collisions."""
    base, ext = os.path.splitext(filename)
    candidate = os.path.join(directory, filename)
    i = 2
    while os.path.exists(candidate):
        candidate = os.path.join(directory, f"{base} ({i}){ext}")
        i += 1
    return candidate


def move_to_output(workdir: str, output_dir: str = OUTPUT_DIR) -> list[str]:
    """Move every file produced in `workdir` into `output_dir`. Return final paths."""
    os.makedirs(output_dir, exist_ok=True)
    final = []
    for root, _dirs, files in os.walk(workdir):
        for f in files:
            src = os.path.join(root, f)
            dst = unique_path(output_dir, f)
            shutil.move(src, dst)
            final.append(dst)
    return final
