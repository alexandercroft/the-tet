"""Video / 1000+ sites via yt-dlp (YouTube, TikTok, X, Vimeo, IG Reels, ...)."""
import os
import yt_dlp

from .common import USER_AGENT, ensure_h264, reset_dir, ydl_cookiesfrombrowser


def run(url: str, workdir: str, job: dict, opts: dict) -> list[str]:
    audio = opts.get("format") == "audio"

    def hook(d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            if total:
                job["progress"] = int(d.get("downloaded_bytes", 0) / total * 100)
        elif d["status"] == "finished":
            job["progress"] = 99  # leave room for post-processing

    ydl_opts = {
        "outtmpl": os.path.join(workdir, "%(title).80s.%(ext)s"),
        "noplaylist": True,
        "progress_hooks": [hook],
        "quiet": True,
        "no_warnings": True,
        "http_headers": {"User-Agent": USER_AGENT},
        "merge_output_format": "mp4",
        "format": "ba/b" if audio else "bv*+ba/b",
        # Prefer h264 so the result plays in QuickTime/Preview; sites like YouTube
        # serve higher resolutions as VP9/AV1, which macOS can't decode. VP9/AV1-only
        # media still downloads and is transcoded by the central ensure_h264 guard.
        "format_sort": ["vcodec:h264"],
    }
    if audio:
        ydl_opts["postprocessors"] = [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}
        ]
    # Browser cookies unlock private / age-gated content; ignore if unavailable.
    try:
        ydl_opts["cookiesfrombrowser"] = ydl_cookiesfrombrowser()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
    except Exception:
        ydl_opts.pop("cookiesfrombrowser", None)
        reset_dir(workdir)  # clear any partial output from the failed first attempt
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

    job["title"] = info.get("title") or job.get("title")
    job["uploader"] = info.get("uploader") or info.get("channel")
    job["thumbnail"] = info.get("thumbnail")
    job["duration"] = info.get("duration")
    files = [os.path.join(workdir, f) for f in os.listdir(workdir)]
    ensure_h264(files, job)  # no-op for audio / already-h264; transcodes VP9/AV1
    return files
