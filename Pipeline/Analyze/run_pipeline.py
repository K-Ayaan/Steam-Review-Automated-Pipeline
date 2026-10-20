"""
End-to-end pipeline for one Steam App ID:

scrape reviews -> preprocess -> Ollama insights -> analysis
-> Gemini ads -> distribution (dry-run unless --live)

Usage (from Pipeline/Analyze):

    python run_pipeline.py --app-id 3297310
"""

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

ANALYZE_ROOT = Path(__file__).resolve().parent

os.chdir(ANALYZE_ROOT)

sys.path.insert(0, str(ANALYZE_ROOT))

sys.path.insert(1, str(ANALYZE_ROOT.parent / "Scraper-main"))

from config.env_loader import load_env

load_env()

import pandas as pd

from main import scrape

from generate_dataset import generate_dataset

from intelligence.genre_engine import GenreEngine

from intelligence.review_insight_extractor import (
    ReviewInsightExtractor
)

from services.steam_market import SteamMarket

from pipeline.run_full_analysis import run_analysis

from dashboard.campaign_manager import CampaignManager

from services.publisher import Publisher


CHANNELS = ["discord", "reddit", "email"]


def build_genre_profile(

    game_name,

    market
):

    profile = GenreEngine().detect(
        game_name
    )

    if profile["genre"] == "Unknown":

        genres = market.get(
            "game",
            {}
        ).get(
            "genres",
            []
        )

        if genres:

            profile = {

                **profile,

                "genre":
                " / ".join(genres)
            }

    return profile


def fill_profile_from_insights(

    profile,

    insights
):

    # Games missing from config/game_profiles.json get
    # pillars and audiences from what players actually said.

    if not profile.get("pillars"):

        profile["pillars"] = [

            t.title()

            for t in insights.get("top_topics", [])[:4]
        ]

    if not profile.get("target_audiences"):

        ranked = sorted(

            insights.get("segments", {}).items(),

            key=lambda kv: kv[1]["count"],

            reverse=True
        )

        profile["target_audiences"] = [

            name

            for name, _ in ranked

            if name != "Other"

        ][:4]

    return profile


def latest_run_dir():

    runs = sorted(
        Path("outputs").glob("run_*")
    )

    return runs[-1] if runs else None


def distribute(

    run_dir,

    live=False,

    channels=CHANNELS
):

    manager = CampaignManager()

    publisher = Publisher()

    campaigns = manager.load(
        run_dir
    )

    results = []

    for campaign in campaigns:

        if campaign.get("platform") not in channels:

            continue

        # Live sends respect the approval workflow;
        # dry-run previews everything.

        if live and campaign.get("status") != "APPROVED":

            continue

        ok = publisher.publish(

            campaign,

            dry_run=not live
        )

        if live and ok:

            campaign["status"] = "PUBLISHED"

            campaign["published_at"] = (
                pd.Timestamp.now().isoformat()
            )

        results.append({

            "campaign_id":
            campaign.get("campaign_id"),

            "platform":
            campaign.get("platform"),

            "ok":
            bool(ok)
        })

    if live:

        manager.save(
            run_dir,
            campaigns
        )

    return results


def run(args):

    if not args.skip_scrape:

        print(f"\n[1/6] Scraping reviews for app {args.app_id}")

        scrape(

            args.app_id,

            max_pages=args.max_pages,

            max_reviews=args.max_reviews
        )

    reviews = pd.read_csv(
        "data/reviews.csv"
    )

    game_name = str(
        reviews["game_name"].iloc[0]
    )

    print(f"\n[2/6] Preprocessing {len(reviews)} reviews of {game_name}")

    df = generate_dataset(
        game_name=game_name
    )

    print("\n[3/6] Fetching Steam market data")

    market = SteamMarket().build_report(

        args.app_id,

        args.competitors
    )

    genre_profile = build_genre_profile(

        game_name,

        market
    )

    print(f"\n[4/6] Ollama insights (genre: {genre_profile['genre']})")

    extractor = ReviewInsightExtractor(

        segments=genre_profile.get(
            "target_audiences"
        )
    )

    sample = (

        df.drop_duplicates("review_text")

        .head(args.max_reviews)
    )

    rows = extractor.extract_all(
        sample
    )

    pd.DataFrame(rows).to_csv(

        "data/review_insights.csv",

        index=False,

        encoding="utf-8-sig"
    )

    insights = extractor.summarize(
        rows
    )

    genre_profile = fill_profile_from_insights(

        genre_profile,

        insights
    )

    print("\n[5/6] Analysis + ad generation")

    before = latest_run_dir()

    run_analysis(

        app_id=str(args.app_id),

        start_date=args.start_date,

        end_date=args.end_date,

        game_version=args.version,

        genre_profile=genre_profile,

        insights=insights
    )

    run_dir = latest_run_dir()

    if run_dir is None or run_dir == before:

        raise RuntimeError(
            "Analysis produced no run folder"
        )

    with open(

        run_dir / "market_report.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            market,

            f,

            ensure_ascii=False,

            indent=4
        )

    if args.skip_distribute:

        print("\n[6/6] Distribution skipped")

        return run_dir, []

    mode = "LIVE" if args.live else "DRY-RUN"

    print(f"\n[6/6] Distribution ({mode})")

    results = distribute(

        run_dir,

        live=args.live,

        channels=args.channels
    )

    print(

        f"\nDone. Run: {run_dir} | "

        f"{sum(r['ok'] for r in results)}/{len(results)} "

        f"campaigns {mode.lower()} OK"
    )

    return run_dir, results


def parse_args(argv=None):

    parser = argparse.ArgumentParser(
        description="Steam App ID -> reviews -> insights -> ads -> distribution"
    )

    parser.add_argument("--app-id", type=int, required=True)

    parser.add_argument("--max-pages", type=int, default=20)

    parser.add_argument("--max-reviews", type=int, default=200)

    parser.add_argument("--start-date", default="2000-01-01")

    parser.add_argument("--end-date", default=str(date.today()))

    parser.add_argument("--version", default=None)

    parser.add_argument("--competitors", type=int, nargs="*", default=None)

    parser.add_argument("--channels", nargs="*", default=CHANNELS, choices=CHANNELS)

    parser.add_argument("--skip-scrape", action="store_true",
                        help="reuse data/reviews.csv")

    parser.add_argument("--skip-distribute", action="store_true")

    parser.add_argument("--live", action="store_true",
                        help="actually send APPROVED campaigns (default: dry-run)")

    return parser.parse_args(argv)


if __name__ == "__main__":

    run(parse_args())
