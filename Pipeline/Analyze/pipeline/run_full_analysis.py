import pandas as pd
import sys
import os
from utils.run_manager import (
    RunManager
)
from reports.report_exporter import (
    ReportExporter
)
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(
    PROJECT_ROOT
)

from config.env_loader import (
    load_env
)

load_env()

import json

from intelligence.llm_report_writer import (
    LLMReportWriter
)

from intelligence.executive_summary import (
    ExecutiveSummary
)

from reports.executive_summary_generator import (
    ExecutiveSummaryGenerator
)

from intelligence.game_health_score import (
    GameHealthScore
)

from reports.evidence_report_generator import (
    EvidenceReportGenerator
)

from reports.developer_report_generator import (
    DeveloperReportGenerator
)

from intelligence.rule_based_extractor import (
    RuleBasedExtractor
)

from intelligence.llm_issue_extractor import (
    LLMIssueExtractor
)

from intelligence.issue_database import (
    IssueDatabase
)

from intelligence.report_generator import (
    ReportGenerator
)

from intelligence.developer_agent import (
    DeveloperAgent
)

from intelligence.audience_segmentation import (
    AudienceSegmentation
)

from intelligence.marketing_intelligence import (
    MarketingIntelligence
)

from intelligence.audience_profiler import (
    AudienceProfiler
)

from marketing.campaign_generator import (
    CampaignGenerator
)

from intelligence.genre_detector import (
    GenreDetector
)

from intelligence.review_filter import (
    ReviewFilter
)

from intelligence.player_segmenter import (
    PlayerSegmenter
)

from reports.player_segment_report import (
    PlayerSegmentReport
)

from intelligence.ad_generator import (
    AdGenerator
)

from intelligence.campaign_ranker import (
    CampaignRanker
)

from reports.trend_report_generator import (
    TrendReportGenerator
)

from reports.analysis_metadata import (
    AnalysisMetadata
)

from reports.update_impact_report import (
    UpdateImpactReport
)

from reports.release_summary_generator import (
    ReleaseSummaryGenerator
)

from reports.ai_executive_insights import (
    AIExecutiveInsights
)

from reports.campaign_ranking_generator import (
    CampaignRankingGenerator
)

from reports.version_trend_analyzer import (
    VersionTrendAnalyzer
)

from reports.review_impact_report import (
    ReviewImpactReport
)

from intelligence.marketing_confidence_engine import (
    MarketingConfidenceEngine
)

from reports.segment_campaign_generator import (
    SegmentCampaignGenerator
)

from intelligence.genre_engine import (
    GenreEngine
)

from reports.pdf_exporter import (
    PDFExporter
)

from reports.campaign_planner import (
    CampaignPlanner
)

from intelligence.utm_generator import (
    UTMGenerator
)

from intelligence.creative_generator import (
    CreativeGenerator
)

from intelligence.gemini_creative_generator import (
    GeminiCreativeGenerator,
    channel_creatives
)

from services.link_tracker import (
    LinkTracker
)

from intelligence.creative_generator import(
    CreativeGenerator
)

def run_analysis(

    app_id=None,

    start_date=None,

    end_date=None,

    game_version=None,

    genre_profile=None,

    insights=None
):

    # Arguments override config/analysis_config.json
    # so run_pipeline.py can drive a run from an App ID.

    run_manager = (
        RunManager()
    )

    run_dir = (
        run_manager.create_run_folder()
    )

    print(
        f"Run Directory: {run_dir}"
    )

    df = pd.read_csv(
        "data/language_reviews.csv"
    )

    df["date_posted"] = pd.to_datetime(

        df["date_posted"],

        errors="coerce"
    )

    with open(

        "config/analysis_config.json",

        "r",

        encoding="utf-8"

    ) as f:

        config = json.load(f)

    app_id = (
        app_id
        or
        config[
            "app_id"
        ]
    )

    start_date = pd.to_datetime(

        start_date
        or
        config[
            "review_start_date"
        ]
    )

    end_date = pd.to_datetime(

        end_date
        or
        config[
            "review_end_date"
        ]
    )

    game_version = (
        game_version
        or
        config[
            "game_version"
        ]
    )

    if end_date <= start_date:

        raise ValueError(

            "review_end_date must be after review_start_date"
        )

    df = df[

        (df["date_posted"] >= start_date)

        &

        (df["date_posted"] <= end_date)
    ]

    print(

        f"\nDate Range: "

        f"{start_date.date()} "

        f"to "

        f"{end_date.date()}"
    )

    print(

        f"Reviews After Filter: "

        f"{len(df)}"
    )

    if len(df) == 0:

        print(
            "No reviews found in selected date range."
        )

        return

    rule_engine = (
        RuleBasedExtractor()
    )

    llm_engine = (
        LLMIssueExtractor()
    )

    issue_db = (
        IssueDatabase()
    )

    report_generator = (
        ReportGenerator()
    )

    developer_agent = (
        DeveloperAgent()
    )

    evidence_generator = (
        EvidenceReportGenerator()
    )

    health_engine = (
        GameHealthScore()
    )

    marketing_confidence_engine = (
        MarketingConfidenceEngine()
    )

    impact_predictor = (
        ReviewImpactReport()
    )

    pdf_exporter = (
        PDFExporter()
    )

    summary_generator = (
        ExecutiveSummaryGenerator()
    )

    metadata_generator = (
        AnalysisMetadata()
    )

    impact_generator = (
        UpdateImpactReport()
    )

    release_generator = (
        ReleaseSummaryGenerator()
    )

    ai_insights_generator = (
        AIExecutiveInsights()
    )

    utm_generator = (
        UTMGenerator()
    )

    run_manager = (
        RunManager()
    )

    review_filter = (
        ReviewFilter()
    )

    segmenter = (
        PlayerSegmenter()
    )

    segment_report_generator = (
        PlayerSegmentReport()
    )

    campaign_planner = (
        CampaignPlanner()
    )

    ad_generator = (
        AdGenerator()
    )

    campaign_ranker = (
        CampaignRanker()
    )

    trend_generator = (
        TrendReportGenerator()
    )

    campaign_ranking_generator = (
        CampaignRankingGenerator()
    )

    segment_campaign_generator = (
        SegmentCampaignGenerator()
    )

    genre_engine = (
        GenreEngine()
    )

    version_trend_analyzer = (
        VersionTrendAnalyzer()
    )

    strategy_generator = (
        CreativeGenerator()
    )

    link_tracker = (
        LinkTracker()
    )

    try:

        gemini_creative_generator = (
            GeminiCreativeGenerator()
        )

    except ValueError as e:

        print(
            f"Gemini unavailable ({e}); "
            f"falling back to Ollama creatives"
        )

        gemini_creative_generator = None

    audience_creatives = {}

    creative_generator = (
        CreativeGenerator()
    )

    version_trends = (
        version_trend_analyzer.generate()
    )

    print(
        f"Loaded {len(df)} reviews"
    )

    unknown_reviews = []

    rule_matches = 0

    llm_matches = 0

    seen_reviews = set()

    if len(df) == 0:

        print(
            "No reviews found in selected date range."
        )

        return

    game_name = (
        df["game_name"].iloc[0]
    )

    if genre_profile is None:

        genre_profile = (

            genre_engine.detect(

                game_name=game_name
            )
        )

    # Rules must be loaded before extraction,
    # otherwise every review falls through to the LLM.

    rule_engine.load_rules(

        genre_profile[
            "genre"
        ]
    )

    for idx, row in df.iterrows():

        # if idx > 50:
        #     break

        print(
            f"Processing {idx + 1}/{len(df)}"
        )

        review_text = row[
            "review_text"
        ]

        if review_text in seen_reviews:

            continue

        seen_reviews.add(
            review_text
        )

        if review_filter.should_skip(
            review_text
        ):

            continue

        

        result = (

            rule_engine.extract(

                row["review_text"]
            )
        )

        if (

            result["issues"][0]

            ["issue_id"]

            ==

            "NO_ISSUE"
        ):

            result = (

                llm_engine.extract(

                    row["review_text"]
                )
            )

            llm_matches += 1

        else:

            rule_matches += 1

        if any(
            issue["issue_id"] == "NO_ISSUE"
            for issue in result["issues"]
        ):

            unknown_reviews.append({

                "review_id":
                row["review_id"],

                "game_name":
                row["game_name"],

                "review_text":
                row["review_text"],

                "language":
                row["language"],

                "player_segment":
                row["player_segment"],

                "is_positive":
                row["is_positive"]
            })

        issue_db.add_review(

            issues=result["issues"],

            review_text=row["review_text"],

            language=row["language"],

            player_segment=(

                segmenter.segment(

                    row["hours_played"]
                )
            ),

            impact_score=row[
                "impact_score"
            ],

            helpful_count=row[
                "helpful_count"
            ]
        )

    unknown_df = pd.DataFrame(
        unknown_reviews
    )

    unknown_df.to_csv(

        "data/unknown_reviews.csv",

        index=False
    )

    print(
        f"Saved {len(unknown_df)} unknown reviews"
    )

    known_reviews = (

        len(df)

        -

        len(unknown_reviews)

    )

    report = (
        report_generator.generate(

            issue_db.summary(),

            known_reviews,

            df["game_name"].iloc[0]
        )
    )

    segment_report = (

        segment_report_generator.generate(

            issue_db.summary()
        )
    )


    genre_detector = (
        GenreDetector()
    )

    genre = (

        genre_detector.detect(

            df["game_name"].iloc[0],

            # report
        )
    )

    print(
        f"\nGENRE: {genre}"
    )

    segmenter = (
        AudienceSegmentation()
    )

    audience_report = (

        segmenter.generate(
            report
        )
    )

    profiler = (
        AudienceProfiler()
    )


    audience_report[
        "target_audiences"
    ] = (

        profiler.profile(

            # df["game_name"].iloc[0],

            report,

            genre_profile
        )
    )

    marketing_engine = (
        MarketingIntelligence()
    )

    known_reviews = (

        len(df)

        -

        len(unknown_reviews)

    )

    metadata = (

        metadata_generator.generate(

            game_name=
            df["game_name"].iloc[0],

            review_count=
            len(df),

            known_reviews=
            known_reviews,

            unknown_reviews=
            len(unknown_reviews),

            start_date=
            start_date,

            end_date=
            end_date,

            version=
            game_version
        )
    )

    

    audience_report[
        "report"
    ] = report

    marketing_report = (

        marketing_engine.generate(

            audience_report,
            known_reviews,
            genre_profile
        )
    )

    review_impact_report = (

        impact_predictor.generate(

            report
        )
    )

    marketing_report[
        "high_risk_issues"
    ] = [

        item["issue_id"]

        for item in report

        if item["severity"] in [

            "CRITICAL",

            "HIGH"
        ]
    ]

    

    campaign_generator = (
        CampaignGenerator()
    )

    campaign_report = (

        campaign_generator.generate(

            marketing_report
        )
    )

    segment_campaigns = (

        segment_campaign_generator.generate(

            audience_report,

            campaign_report
        )
    )



    for campaign in (

        segment_campaigns
    ):

        campaign["tracking"] = (

            utm_generator.generate(

                campaign["audience"],

                campaign["channel"],

                game_name
            )
        )

        tracking = campaign[
            "tracking"
        ]

        campaign["tracking_url"] = (

            f"https://store.steampowered.com/app/{app_id}"

            f"?utm_source={tracking['utm_source']}"

            f"&utm_medium={tracking['utm_medium']}"

            f"&utm_campaign={tracking['utm_campaign']}"
        )

        if gemini_creative_generator:

            audience = campaign[
                "audience"
            ]

            if audience not in audience_creatives:

                audience_creatives[audience] = (

                    gemini_creative_generator.generate({

                        "game_name":
                        game_name,

                        "genre":
                        genre_profile["genre"],

                        "pillars":
                        genre_profile["pillars"],

                        "audience":
                        audience,

                        "promote":
                        campaign["promote"],

                        "avoid":
                        marketing_report["avoid"],

                        "insights":
                        (insights or {}).get(
                            "segments",
                            {}
                        ).get(
                            audience,
                            insights or {}
                        )
                    })
                )

            campaign["creatives"] = (

                channel_creatives(

                    audience_creatives[audience],

                    campaign["platform"]
                )
            )

            campaign["generated_by"] = (
                "gemini"
            )

        else:

            campaign["creatives"] = (

                creative_generator.generate(

                    campaign,

                    marketing_report,

                    genre_profile,

                    game_name=game_name
                )
            )

            campaign["generated_by"] = (
                "ollama"
            )

        creatives = campaign[
            "creatives"
        ]

        campaign["headline"] = (

            creatives.get(

                "headline",

                ""
            )
        )

        campaign["cta"] = (

            creatives.get(

                "cta",

                ""
            )
        )

        campaign["ad_copy"] = (

            creatives.get(

                "ad_copy",

                ""
            )
        )

        campaign["campaign_id"] = (

            f"{game_name}_"

            f"{campaign['audience']}_"

            f"{campaign['channel']}"
        )

        campaign["campaign_id"] = (

            campaign["campaign_id"]

            .lower()

            .replace(" ", "_")

            .replace("/", "_")
        )

        campaign["short_code"] = (

            link_tracker.generate(

                campaign["campaign_id"],

                campaign["tracking_url"]
            )
        )

        campaign["tracked_url"] = (

            f"http://localhost:8000/r/"

            f"{campaign['short_code']}"
        )

        campaign["status"] = (
            "PENDING"
        )

        campaign["impressions"] = 0

        campaign["clicks"] = 0

        campaign["visits"] = 0

        campaign["wishlists"] = 0

        campaign["downloads"] = 0

        campaign["spend"] = 0

    print(
        "\nMARKETING INTELLIGENCE"
    )

    print(
        "\nTarget Audiences:"
    )

    for audience in (

        marketing_report[
            "target_audiences"
        ]
    ):  

        print(
            f"- {audience}"
        )

    print(
        "\nPromote:"
    )

    for angle in (

        marketing_report[
            "angles"
        ]
    ):

        print(
            f"- {angle}"
        )

    print(
        "\nAvoid:"
    )

    for item in (

        marketing_report[
            "avoid"
        ]
    ):

        print(
            f"- {item}"
        )

    for issue in report:

        issue["top_reviews"] = (

            issue_db.get_top_reviews(

                issue["issue_id"]

            )
        )

    health_engine = (
        GameHealthScore()
    )

    trend_report = (
        trend_generator.generate()
    )

    game_metadata = {

        "game_name":
        df["game_name"].iloc[0],

        "genre":
        genre,

        "review_count":
        len(df),

        "known_reviews":
        known_reviews,

        "unknown_reviews":
        len(unknown_reviews)
    }

    print(
        f"Known Reviews: {known_reviews}"
    )

    print(
        f"Rule Matches: {rule_matches}"
    )

    print(
        f"LLM Matches: {llm_matches}"
    )

    print(
        "\nAUDIENCE SEGMENTS"
    )

    for audience in (

        audience_report[
            "target_audiences"
        ]
    ):

        print(
            f"- {audience}"
        )

    print("\nTOP ISSUES")

    for issue in report[:3]:

        print(

            issue["issue_id"],

            issue["count"]
        )

    positive_reviews = len(

        df[
            df["is_positive"] == True
        ]

    )

    total_reviews = len(df)

    health_scores = (
        health_engine.calculate(

            report,

            known_reviews,

            positive_reviews,

            total_reviews
        )
    )

    marketing_confidence = (

        marketing_confidence_engine.calculate(

            health_scores,

            report
        )
    )

    campaign_plan = (

        campaign_planner.generate(

            campaign_report,

            audience_report,

            marketing_confidence
        )
    )

    ads = (

        ad_generator.generate(

            df["game_name"].iloc[0],

            marketing_report,

            marketing_confidence,

            health_scores,

            genre_profile

        )
    )


    campaigns = (

        campaign_ranker.rank(

            marketing_report,

            health_scores
        )
    )

    campaign_ranking = (

        campaign_ranking_generator.generate(

            report,

            health_scores
        )
    )

    summary_engine = (
        ExecutiveSummary()
    )

    executive_summary = (

        summary_engine.generate(

            report,

            health_scores,

            28.0,

            len(df)
        )
    )

    print(
        "\nGAME HEALTH"
    )

    summary = (
        summary_generator.generate(
            report,
            health_scores
        )
    )

    with open(

        run_dir /
        "health_scores.json",

        "w"

    ) as f:

        json.dump(

            health_scores,

            f,

            indent=4
        )

    with open(

        run_dir /

        "review_impact_report.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            review_impact_report,

            f,

            indent=4
        )

    with open(

        run_dir /

        "analysis_metadata.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            metadata,

            f,

            ensure_ascii=False,

            indent=4,

            default=str
        )

    with open(

        run_dir /

        "game_metadata.json",

        "w"

    ) as f:

        json.dump(

            game_metadata,

            f,

            indent=4
        )

    with open(

        run_dir /

        "audience_report.json",

        "w"

    ) as f:

        json.dump(

            audience_report,

            f,

            indent=4
        )

    with open(

        run_dir /

        "issues.json",

        "w"

    ) as f:

        json.dump(

            report,

            f,

            indent=4
        )

    with open(

        str(
            run_dir /
            "executive_summary.txt"
        ),

        "w",

        encoding="utf-8"

    ) as f:

        f.write(
            summary
        )

    with open(

        run_dir /

        "marketing_report.json",

        "w"

    ) as f:

        json.dump(

            marketing_report,

            f,

            indent=4
        )

    with open(

        run_dir /

        "campaign_report.json",

        "w"

    ) as f:

        json.dump(

            campaign_report,

            f,

            indent=4
        )

    with open(

        str(
            run_dir /
            "player_segment_report.txt"
        ),

        "w",

        encoding="utf-8"

    ) as f:

        f.write(
            segment_report
        )

    with open(

        run_dir /

        "ad_campaigns.txt",

        "w",

        encoding="utf-8"

    ) as f:

        f.write(
            ads
        )

    with open(

        run_dir /

        "campaign_rankings.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            campaigns,

            f,

            ensure_ascii=False,

            indent=4
        )

    with open(

        run_dir /

        "marketing_report.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            marketing_report,

            f,

            ensure_ascii=False,

            indent=4
        )

    with open(

        run_dir /

        "trend_report.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            trend_report,

            f,

            indent=4
        )

    with open(

        run_dir /

        "version_trend_report.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            version_trends,

            f,

            indent=4
        )

    with open(

        run_dir /

        "marketing_confidence.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            marketing_confidence,

            f,

            indent=4
        )

    with open(

        run_dir /

        "segment_campaigns.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            segment_campaigns,

            f,

            indent=4
        )

    if insights:

        with open(

            run_dir /

            "insights.json",

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                insights,

                f,

                ensure_ascii=False,

                indent=4
            )

    with open(

        run_dir /

        "genre_profile.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            genre_profile,

            f,

            indent=4
        )

    with open(

        run_dir /

        "campaign_plan.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            campaign_plan,

            f,

            indent=4
        )

    for metric, value in (
        health_scores.items()
    ):

        print(
            f"{metric}: {value}"
        )

    evidence_report = (

        evidence_generator.generate(
            issue_db.summary()
        )

    )

    with open(

        "reports/evidence_report.txt",

        "w",

        encoding="utf-8"

    ) as f:

        f.write(
            evidence_report
        )

    print("\nEXECUTIVE SUMMARY")

    print(
        f"Overall Health: "
        f"{executive_summary['overall_health']}"
    )

    print(
        f"Review Score: "
        f"{executive_summary['review_score']}%"
    )

    writer = (
        LLMReportWriter()
    )

    executive_report = (

        writer.generate(

            report,

            health_scores

        )
    )

    print(
        "\nEXECUTIVE REPORT"
    )

    print(
        "=" * 50
    )

    print(
        executive_report
    )

    print("\nTop Issues:")

    for issue in (
        executive_summary["top_issues"]
    ):

        print(
            f"- {issue}"
        )

    developer_report_generator = (
        DeveloperReportGenerator()
    )


    developer_report = (
        developer_report_generator.generate(
            report[:10]
        )
    )

    print("koko",
        developer_report
    )

    with open(

        str(
            run_dir /
            "developer_report.txt"
        ),

        "w",

        encoding="utf-8"

    ) as f:

        f.write(
            developer_report
        )

    exporter = (
        ReportExporter()
    )

    exporter.export_developer_report(

        report,

        str(
            run_dir /
            "developer_report.csv"
        )
    )

    for issue in report:

        print("\n" + "=" * 50)

        print(
            f"Issue: {issue['issue_id']}"
        )

        print(
            f"Severity: {issue['severity']}"
        )

        print(
            f"Priority: {issue['priority']}"
        )

        print(
            f"Department: {issue['department']}"
        )

        print(
            f"Team: {issue['team']}"
        )

        print(
            f"Category: {issue['category']}"
        )

        print(
            f"Mentions: {issue['count']}"
        )

        print(
            f"Impact: {issue['impact_score']}"
        )

        print(
            f"Helpful Votes: {issue['helpful_count']}"
        )

        top_reviews = (

            issue_db.get_top_reviews(

                issue["issue_id"]
            )
        )

        print(
            "Developer Actions:"
        )

        for action in developer_agent.recommend(
            issue["issue_id"]
        ):

            print(
                f" - {action}"
            )

    impact_report = (

        impact_generator.generate()
    )

    release_summary = (

        release_generator.generate(

            health_scores,

            audience_report,

            campaign_report,

            impact_report
        )
    )

    ai_insights = (

        ai_insights_generator.generate(

            executive_summary,

            impact_report,

            audience_report,

            campaign_report
        )
    )

    with open(

        run_dir /

        "update_impact_report.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            impact_report,

            f,

            indent=4
        )

    with open(

        run_dir /

        "release_summary.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            release_summary,

            f,

            indent=4
        )

    with open(

        run_dir /

        "ai_insights.txt",

        "w",

        encoding="utf-8"

    ) as f:

        f.write(
            ai_insights
        )

    with open(

        run_dir /

        "campaign_rankings.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            campaign_ranking,

            f,

            indent=4
        )

    game_name=df["game_name"].iloc[0]

    

    pdf_exporter.export(

        run_dir /
        "executive_report.pdf",

        metadata,

        health_scores,

        report,

        audience_report,

        campaign_report,

        executive_summary,

        ai_insights,

        segment_campaigns
    )
        
    return report

if __name__ == "__main__":

    run_analysis()


    