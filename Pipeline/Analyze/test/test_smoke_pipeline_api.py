import os
import sys

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

import pytest

from fastapi.testclient import TestClient

from services import pipeline_api


TOKEN = "test-token"


class FakeProcess:

    def __init__(self, args, **kw):

        self.args = args

        self.code = None

    def poll(self):

        return self.code


@pytest.fixture
def client(monkeypatch, tmp_path):

    monkeypatch.setenv("PIPELINE_API_TOKEN", TOKEN)

    monkeypatch.setattr(pipeline_api, "LOG_DIR", tmp_path)

    monkeypatch.setattr(pipeline_api, "jobs", {})

    started = []

    def fake_popen(args, **kw):

        process = FakeProcess(args)

        started.append(process)

        return process

    monkeypatch.setattr(pipeline_api.subprocess, "Popen", fake_popen)

    client = TestClient(pipeline_api.app)

    client.started = started

    return client


def test_requires_token(client, monkeypatch):

    assert client.post("/runs", json={"app_id": 1}).status_code == 401

    monkeypatch.delenv("PIPELINE_API_TOKEN")

    response = client.post(
        "/runs", json={"app_id": 1}, headers={"X-API-Key": TOKEN}
    )

    assert response.status_code == 503


def test_starts_dry_run_only(client):

    response = client.post(
        "/runs",
        json={"app_id": 3297310, "max_reviews": 50},
        headers={"X-API-Key": TOKEN}
    )

    assert response.status_code == 202

    assert response.json()["mode"] == "dry-run"

    args = client.started[0].args

    assert "--live" not in args

    assert args[args.index("--app-id") + 1] == "3297310"

    assert args[args.index("--max-reviews") + 1] == "50"


def test_review_cap_and_single_run(client):

    headers = {"X-API-Key": TOKEN}

    too_many = client.post(
        "/runs", json={"app_id": 1, "max_reviews": 501}, headers=headers
    )

    assert too_many.status_code == 422

    job_id = client.post(
        "/runs", json={"app_id": 1}, headers=headers
    ).json()["job_id"]

    assert client.post(
        "/runs", json={"app_id": 2}, headers=headers
    ).status_code == 409

    client.started[0].code = 0

    status = client.get(f"/runs/{job_id}", headers=headers).json()

    assert status["status"] == "succeeded"

    assert client.post(
        "/runs", json={"app_id": 2}, headers=headers
    ).status_code == 202
