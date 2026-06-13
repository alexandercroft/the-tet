"""The TET — universal media extractor. Local Flask server."""
import os
import shutil
import subprocess
import tempfile
import threading
import uuid

from flask import Flask, jsonify, render_template, request

from tet import detect as detect_mod, file, instagram, telegram, threads, video
from tet.common import OUTPUT_DIR, ensure_h264, move_to_output
from tet.logo import LOGO_DATA_URI

ENGINES = {
    "video": video.run,
    "instagram": instagram.run,
    "threads": threads.run,
    "telegram": telegram.run,
    "file": file.run,
}

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
jobs: dict[str, dict] = {}


def run_job(job_id: str, url: str, source: str, opts: dict):
    job = jobs[job_id]
    workdir = tempfile.mkdtemp(prefix="tet_")
    try:
        produced = ENGINES[source](url, workdir, job, opts)
        if not produced:
            raise RuntimeError("Nothing was downloaded")
        ensure_h264(produced, job)  # any non-h264 (VP9/AV1) → h264 so it plays on Apple
        final = move_to_output(workdir, OUTPUT_DIR)
        job["files"] = [os.path.basename(p) for p in final]
        job["paths"] = final
        job["progress"] = 100
        job["status"] = "done"
    except Exception as e:  # surface the real reason to the UI
        msg = str(e).strip().splitlines()[-1] if str(e).strip() else e.__class__.__name__
        job["status"] = "error"
        job["error"] = msg
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


@app.route("/")
def index():
    return render_template("index.html", logo=LOGO_DATA_URI, output_dir=_short(OUTPUT_DIR))


@app.route("/api/detect")
def api_detect():
    return jsonify({"source": detect_mod.detect(request.args.get("url", ""))})


@app.route("/api/extract", methods=["POST"])
def api_extract():
    data = request.get_json(force=True)
    url = (data.get("url") or "").strip()
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    source = detect_mod.detect(url)
    job_id = uuid.uuid4().hex[:8]
    jobs[job_id] = {
        "status": "working", "progress": None, "source": source,
        "url": url, "title": None, "uploader": None, "thumbnail": None,
        "duration": None, "files": [], "error": None,
    }
    opts = {"format": data.get("format", "video")}
    t = threading.Thread(target=run_job, args=(job_id, url, source, opts), daemon=True)
    t.start()
    return jsonify({"job_id": job_id, "source": source})


@app.route("/api/status/<job_id>")
def api_status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify({k: job.get(k) for k in (
        "status", "progress", "source", "title", "uploader",
        "thumbnail", "duration", "files", "error",
    )})


@app.route("/api/reveal", methods=["POST"])
def api_reveal():
    job = jobs.get((request.get_json(force=True) or {}).get("job_id", ""))
    target = job["paths"][0] if job and job.get("paths") else OUTPUT_DIR
    try:
        subprocess.run(["open", "-R", target], check=False)
    except Exception:
        subprocess.run(["open", OUTPUT_DIR], check=False)
    return jsonify({"ok": True})


def _short(path: str) -> str:
    home = os.path.expanduser("~")
    return path.replace(home, "~") if path.startswith(home) else path


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8900))
    print(f"\n  The TET is running at http://127.0.0.1:{port}\n")
    app.run(host="127.0.0.1", port=port)
