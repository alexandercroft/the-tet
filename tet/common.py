"""Shared helpers: output dir, filename safety, browser cookies, file moves."""
import os
import re
import shutil
import subprocess

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


def reset_dir(directory: str) -> None:
    """Drop any partial leftovers so a failed attempt can't cause duplicates."""
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)
        else:
            try:
                os.remove(path)
            except OSError:
                pass


def ensure_h264(files: list[str], job: dict) -> None:
    """Transcode any non-h264 video to h264 in place so Apple players (QuickTime,
    Preview, native Telegram decode) can render it. Sites like Instagram/YouTube
    serve higher resolutions as VP9/AV1, which macOS cannot decode — audio plays
    but the picture freezes. No-op when the video is already h264 (the common case,
    since the yt-dlp engines prefer it via format_sort), so a transcode only fires
    on VP9/AV1-only media. ffmpeg is already on PATH (yt-dlp uses it to merge)."""
    for path in files:
        if not path.lower().endswith((".mp4", ".mov", ".mkv", ".webm")):
            continue
        try:
            codec = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=codec_name", "-of", "csv=p=0", path],
                capture_output=True, text=True, timeout=30,
            ).stdout.strip()
        except Exception:
            continue
        if codec in ("", "h264"):
            continue
        job["progress"] = None  # indeterminate: transcoding
        tmp = path + ".h264.mp4"
        r = subprocess.run(
            ["ffmpeg", "-y", "-i", path,
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
             "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", tmp],
            capture_output=True, text=True,
        )
        if r.returncode == 0 and os.path.exists(tmp) and os.path.getsize(tmp) > 0:
            os.replace(tmp, path)  # keep the original filename
        elif os.path.exists(tmp):
            os.remove(tmp)


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
