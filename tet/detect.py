"""Map a URL to the extractor that should handle it."""
import re

VIDEO_HOSTS = (
    "youtube.com", "youtu.be", "tiktok.com", "twitter.com", "x.com",
    "vimeo.com", "facebook.com", "fb.watch", "reddit.com", "twitch.tv",
    "dailymotion.com", "soundcloud.com", "streamable.com", "vk.com",
    "ok.ru", "bilibili", "rutube", "pinterest", "tumblr.com", "loom.com",
)

FILE_EXT = re.compile(
    r"\.(mp4|mov|mkv|webm|avi|mp3|m4a|wav|flac|ogg|jpg|jpeg|png|gif|webp|"
    r"pdf|zip|rar|7z|docx?|xlsx?|pptx?|csv|txt|gz|tar|dmg|exe|apk|epub)$"
)


def detect(url: str) -> str:
    """Return one of: threads, instagram, telegram, file, video."""
    u = url.lower().strip()
    if "threads.com" in u or "threads.net" in u:
        return "threads"
    if "instagram.com" in u or "instagr.am" in u:
        return "instagram"
    if "t.me/" in u or "telegram.me/" in u:
        return "telegram"
    if any(h in u for h in VIDEO_HOSTS):
        return "video"
    if FILE_EXT.search(u.split("?")[0]):
        return "file"
    # Unknown host: yt-dlp supports 1000+ sites, so let it try.
    return "video"
