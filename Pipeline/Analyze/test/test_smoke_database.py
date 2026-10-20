import json
import os
import sys

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

import pytest

from database import campaign_repository
from database.campaign_repository import CampaignRepository


RUN_ID = "run_2000-01-01_00-00-00"


@pytest.fixture
def run_dir(tmp_path):

    folder = tmp_path / RUN_ID

    folder.mkdir()

    files = {

        "analysis_metadata.json": {
            "game_name": "Smoke Game",
            "analysis_date": "2000-01-01",
            "review_count": 2
        },

        "insights.json": {"count": 2},

        "issues.json": [
            {"issue_id": "CRASHES", "severity": "HIGH", "count": 2}
        ],

        "segment_campaigns.json": [{
            "campaign_id": "smoke_game_horror_fans_email",
            "audience": "Horror Fans",
            "platform": "email",
            "status": "PENDING",
            "short_code": "smoke123",
            "tracking_url": "https://store.steampowered.com/app/1",
            "creatives": {"headline": "H"},
            "clicks": 3
        }]
    }

    for name, data in files.items():

        (folder / name).write_text(
            json.dumps(data),
            encoding="utf-8"
        )

    return folder


def test_no_database_url_is_a_no_op(monkeypatch, run_dir):

    monkeypatch.delenv("DATABASE_URL", raising=False)

    monkeypatch.setattr(
        campaign_repository.psycopg,
        "connect",
        lambda *a, **kw: pytest.fail("connected without DATABASE_URL")
    )

    repo = CampaignRepository()

    assert repo.save_run(run_dir, 1) is None

    assert repo.log_approval("x", "APPROVED") is False

    assert repo.log_publish("x", "email", "SUCCESS") is False


def test_unreachable_database_does_not_raise(run_dir, capsys):

    repo = CampaignRepository(
        "postgresql://nobody:secret-pw@127.0.0.1:1/none"
    )

    assert repo.save_run(run_dir, 1) is None

    out = capsys.readouterr().out

    assert "Postgres unavailable" in out

    assert "secret-pw" not in out


@pytest.mark.skipif(
    not os.getenv("TEST_DATABASE_URL"),
    reason="set TEST_DATABASE_URL to a disposable Postgres to run"
)
def test_round_trip_against_postgres(run_dir):

    repo = CampaignRepository(
        os.environ["TEST_DATABASE_URL"]
    )

    assert repo.save_run(run_dir, 1)["campaigns"] == 1

    # Re-mirroring the same run must not fail on conflicts.

    assert repo.save_run(run_dir, 1)

    assert repo.log_approval(
        "smoke_game_horror_fans_email", "APPROVED", RUN_ID
    )

    assert repo.log_publish(
        "smoke_game_horror_fans_email", "email", "SUCCESS", "ok"
    )

    with repo.connect() as conn:

        status, published = conn.execute(
            "SELECT status, published_at FROM campaigns WHERE run_id = %s",
            (RUN_ID,)
        ).fetchone()

        clicks = conn.execute(
            "SELECT clicks FROM campaign_metrics WHERE run_id = %s",
            (RUN_ID,)
        ).fetchone()[0]

        approvals = conn.execute(
            "SELECT count(*) FROM approval_logs WHERE run_id = %s",
            (RUN_ID,)
        ).fetchone()[0]

        # Leave the database as we found it.

        conn.execute(
            "DELETE FROM approval_logs WHERE run_id = %s", (RUN_ID,)
        )

        conn.execute(
            "DELETE FROM publishing_logs WHERE campaign_id = %s",
            ("smoke_game_horror_fans_email",)
        )

        conn.execute("DELETE FROM runs WHERE run_id = %s", (RUN_ID,))

        conn.execute("DELETE FROM games WHERE app_id = 1")

    assert status == "PUBLISHED"

    assert published is not None

    assert clicks == 3

    assert approvals == 1
