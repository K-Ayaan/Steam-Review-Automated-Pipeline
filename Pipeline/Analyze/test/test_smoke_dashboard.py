import os
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest


ANALYZE_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def in_analyze_root(monkeypatch):

    # The dashboard uses paths relative to Pipeline/Analyze

    monkeypatch.chdir(ANALYZE_ROOT)


def test_dashboard_renders_new_views():

    if not list(Path("outputs").glob("run_*/health_scores.json")):

        pytest.skip("no analysis run in outputs/")

    app = AppTest.from_file(

        str(ANALYZE_ROOT / "dashboard" / "app.py"),

        default_timeout=120
    )

    app.run()

    assert not app.exception, [e.message for e in app.exception]

    labels = [tab.label for tab in app.tabs]

    for name in ["💰 Sales", "💬 Sentiment", "🥊 Competitors"]:

        assert name in labels

    headers = [h.value for h in app.header]

    for header in ["Sales", "Player Sentiment", "Competitor Analysis"]:

        assert header in headers
