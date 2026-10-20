import json
import os
import sys

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

import pandas as pd
import requests

from intelligence import review_insight_extractor as rie

from services import steam_market


class FakeResponse:

    def __init__(self, payload):

        self.payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self.payload


def test_insights_validate_and_summarize(monkeypatch, tmp_path):

    monkeypatch.chdir(tmp_path)

    (tmp_path / "data").mkdir()

    answers = iter([

        {"sentiment": "Positive", "emotions": ["fear", "made-up"],
         "topics": ["Atmosphere"], "player_segment": "Horror Fans"},

        {"sentiment": "weird", "emotions": ["frustration"],
         "topics": ["bugs", "crashes"], "player_segment": "Nobody"}
    ])

    monkeypatch.setattr(
        rie.requests,
        "post",
        lambda *a, **kw: FakeResponse({"response": json.dumps(next(answers))})
    )

    extractor = rie.ReviewInsightExtractor(segments=["Horror Fans"])

    df = pd.DataFrame({"review_id": [1, 2], "review_text": ["scary", "buggy"]})

    rows = extractor.extract_all(df)

    assert rows[0]["sentiment"] == "positive"

    assert rows[0]["emotions"] == ["fear"]

    assert rows[1]["sentiment"] == "neutral"

    assert rows[1]["player_segment"] == "Other"

    summary = extractor.summarize(rows)

    assert summary["count"] == 2

    assert summary["segments"]["Horror Fans"]["top_emotions"] == ["fear"]

    # cached: a second extractor must not call Ollama again

    monkeypatch.setattr(rie.requests, "post", lambda *a, **kw: 1 / 0)

    again = rie.ReviewInsightExtractor(segments=["Horror Fans"])

    assert again.extract("scary")["sentiment"] == "positive"


def test_estimate_sales():

    est = steam_market.estimate_sales({

        "owners": "100,000 .. 200,000",

        "price_usd": 10.0,

        "total_positive": 75,

        "total_reviews": 100
    })

    assert est["owners_estimate"] == 150000

    assert est["revenue_estimate_usd"] == 1500000.0

    assert est["positive_ratio"] == 75.0


def test_market_snapshot_and_offline_fallback(monkeypatch, tmp_path):

    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(steam_market, "CACHE_FILE", tmp_path / "data" / "market_cache.json")

    def fake_get(self, url, params=None):

        if "appdetails" in url and "steamspy" not in url:

            return {"10": {"success": True, "data": {
                "name": "Game", "genres": [{"description": "Horror"}],
                "price_overview": {"final": 999}}}}

        if "appreviews" in url:

            return {"query_summary": {"total_positive": 9, "total_negative": 1, "total_reviews": 10}}

        return {"owners": "0 .. 20,000", "ccu": 5, "average_forever": 120}

    monkeypatch.setattr(steam_market.SteamMarket, "get_json", fake_get)

    report = steam_market.SteamMarket().build_report(10, [10, 20])

    game = report["game"]

    assert game["genres"] == ["Horror"]

    assert game["price_usd"] == 9.99

    assert game["owners_estimate"] == 10000

    assert [c["app_id"] for c in report["competitors"]] == [20]

    def offline(self, url, params=None):
        raise requests.ConnectionError("offline")

    monkeypatch.setattr(steam_market.SteamMarket, "get_json", offline)

    cached = steam_market.SteamMarket().snapshot(10)

    assert cached["name"] == "Game"
