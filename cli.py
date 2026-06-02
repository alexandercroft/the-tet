#!/usr/bin/env python
"""The TET — command-line downloader.

Usage:
    python cli.py <URL> [--audio] [-o OUTPUT_DIR]

Auto-detects the source (video / instagram / threads / telegram / file),
downloads with the matching engine, and saves into OUTPUT_DIR
(default: ~/Downloads, or $TET_OUTPUT). Prints the saved file paths.
"""
import argparse
import shutil
import sys
import tempfile

from tet import detect as detect_mod, file, instagram, telegram, threads, video
from tet.common import OUTPUT_DIR, move_to_output

ENGINES = {
    "video": video.run,
    "instagram": instagram.run,
    "threads": threads.run,
    "telegram": telegram.run,
    "file": file.run,
}


def main() -> int:
    ap = argparse.ArgumentParser(prog="tet", description="The TET media downloader")
    ap.add_argument("url", help="link to download")
    ap.add_argument("--audio", action="store_true", help="extract audio (mp3) for video sources")
    ap.add_argument("-o", "--output", default=OUTPUT_DIR, help="output folder")
    args = ap.parse_args()

    source = detect_mod.detect(args.url)
    print(f"[the-tet] source = {source}", file=sys.stderr)

    job: dict = {"progress": None}
    workdir = tempfile.mkdtemp(prefix="tet_")
    try:
        produced = ENGINES[source](args.url, workdir, job, {"format": "audio" if args.audio else "video"})
        if not produced:
            print("[the-tet] nothing downloaded", file=sys.stderr)
            return 1
        final = move_to_output(workdir, args.output)
        print(f"[the-tet] {len(final)} file(s) -> {args.output}", file=sys.stderr)
        for p in final:
            print(p)
        return 0
    except Exception as e:
        msg = str(e).strip().splitlines()[-1] if str(e).strip() else e.__class__.__name__
        print(f"[the-tet] error: {msg}", file=sys.stderr)
        return 1
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
