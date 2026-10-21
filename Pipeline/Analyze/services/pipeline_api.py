"""
HTTP trigger so n8n (or curl) can start a pipeline run.

Runs are always dry-run: live distribution is never exposed here.
Approve and publish from the dashboard (or run_pipeline.py --live).

Usage (from Pipeline/Analyze):

    python -m uvicorn services.pipeline_api:app --host 127.0.0.1 --port 8001
"""

import os
import secrets
import subprocess
import sys
import uuid
from datetime import datetime
from pathlib import Path

ANALYZE_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ANALYZE_ROOT))

from config.env_loader import load_env

load_env()

from fastapi import FastAPI, Header, HTTPException

from pydantic import BaseModel, Field


# Same cap as the "ask first" quota rule for test runs.

MAX_REVIEWS_LIMIT = 500

LOG_DIR = ANALYZE_ROOT / "outputs" / "api_runs"

app = FastAPI(
    title="Steam Review Pipeline API"
)

jobs = {}


class RunRequest(BaseModel):

    app_id: int = Field(gt=0)

    max_reviews: int = Field(200, ge=1, le=MAX_REVIEWS_LIMIT)

    max_pages: int = Field(20, ge=1, le=50)


def check_token(token):

    expected = os.getenv(
        "PIPELINE_API_TOKEN"
    )

    if not expected:

        raise HTTPException(
            503,
            "PIPELINE_API_TOKEN is not set"
        )

    if not secrets.compare_digest(
        token or "",
        expected
    ):

        raise HTTPException(
            401,
            "Invalid API key"
        )


def job_status(job):

    code = job["process"].poll()

    if code is None:

        return "running"

    if not job["log"].closed:

        job["log"].close()

    return "succeeded" if code == 0 else "failed"


@app.get("/health")
def health():

    return {"status": "ok"}


@app.post("/runs", status_code=202)
def start_run(

    request: RunRequest,

    x_api_key: str | None = Header(None)
):

    check_token(x_api_key)

    # One run at a time: every run rewrites data/*.csv.

    for job_id, job in jobs.items():

        if job_status(job) == "running":

            raise HTTPException(
                409,
                f"Run {job_id} is still in progress"
            )

    job_id = uuid.uuid4().hex[:12]

    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    log_path = LOG_DIR / f"{job_id}.log"

    log = open(
        log_path,
        "w",
        encoding="utf-8"
    )

    process = subprocess.Popen(

        [
            sys.executable,
            "run_pipeline.py",
            "--app-id", str(request.app_id),
            "--max-reviews", str(request.max_reviews),
            "--max-pages", str(request.max_pages)
        ],

        cwd=ANALYZE_ROOT,

        stdout=log,

        stderr=subprocess.STDOUT,

        # Unbuffered so GET /runs/{id} shows progress while it runs.

        env={
            **os.environ,
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUNBUFFERED": "1"
        }
    )

    jobs[job_id] = {

        "app_id": request.app_id,

        "started_at": datetime.now().isoformat(),

        "process": process,

        "log": log,

        "log_path": log_path
    }

    return {

        "job_id": job_id,

        "status": "running",

        "mode": "dry-run"
    }


@app.get("/runs/{job_id}")
def get_run(

    job_id: str,

    x_api_key: str | None = Header(None)
):

    check_token(x_api_key)

    job = jobs.get(job_id)

    if job is None:

        raise HTTPException(
            404,
            "Unknown job"
        )

    status = job_status(job)

    tail = []

    if job["log_path"].exists():

        tail = job["log_path"].read_text(

            encoding="utf-8",

            errors="replace"

        ).splitlines()[-20:]

    return {

        "job_id": job_id,

        "app_id": job["app_id"],

        "started_at": job["started_at"],

        "status": status,

        "exit_code": job["process"].poll(),

        "log_tail": tail
    }
