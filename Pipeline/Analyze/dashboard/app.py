import sys
import os
from datetime import datetime

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
import pandas as pd
import streamlit as st
from pathlib import Path
import plotly.express as px
from intelligence.review_translator import (
    ReviewTranslator
)
import subprocess

from dashboard.campaign_manager import (
    CampaignManager
)

from database.campaign_repository import (
    CampaignRepository
)

from intelligence.publishing_queue import (
    PublishingQueue
)

from intelligence.campaign_analytics import (
    CampaignAnalytics
)

from intelligence.metrics_loader import (
    MetricsLoader
)

from intelligence.metrics_updater import (
    MetricsUpdater
)

from services.publisher import (
    Publisher
)

from services.campaign_metrics_sync import (
    CampaignMetricsSync
)

from services.publishing_analytics import (
    PublishingAnalytics
)

all_runs = sorted(

    Path("outputs").glob(
        "run_*"
    ),

    reverse=True
)

runs = []

for run in all_runs:

    if (

        run.joinpath(
            "health_scores.json"
        ).exists()

        and

        run.joinpath(
            "issues.json"
        ).exists()
    ):

        runs.append(run)

latest_run = runs[0]

campaign_manager = (
    CampaignManager()
)

publisher = (
    Publisher()
)

publishing_analytics = (
    PublishingAnalytics()
)

publishing_queue = (
    PublishingQueue()
)

campaign_analytics = (
    CampaignAnalytics()
)

metrics_loader = (
    MetricsLoader()
)

metrics_updater = (
    MetricsUpdater()
)

campaign_sync = (
    CampaignMetricsSync()
)

all_versions = []

for run in runs:

    metadata_file = (

        run /

        "analysis_metadata.json"
    )

    if metadata_file.exists():

        with open(

            metadata_file,

            "r",

            encoding="utf-8"

        ) as f:

            metadata = json.load(f)

        all_versions.append({

            "run":
            run.name,

            **metadata
        })

run_names = [

    run.name

    for run in runs
]

selected_run_name = st.sidebar.selectbox(

    "Select Analysis Run",

    run_names
)

latest_run = next(

    run

    for run in runs

    if run.name == selected_run_name
)

with open(

    latest_run / "health_scores.json",

    "r"

) as f:

    health = json.load(f)

with open(

    latest_run / "issues.json",

    "r"

) as f:

    issues = json.load(f)

with open(

    latest_run /

    "marketing_report.json",

    "r",

    encoding="utf-8"

) as f:

    marketing = json.load(f)


with open(

    latest_run /

    "campaign_rankings.json",

    "r",

    encoding="utf-8"

) as f:

    campaigns = json.load(f)

with open(

    latest_run /

    "game_metadata.json",

    "r"

) as f:

    metadata = json.load(f)

with open(

    latest_run /

    "audience_report.json",

    "r"

) as f:

    audience = json.load(f)

with open(

    latest_run /

    "campaign_report.json",

    "r"

) as f:

    campaign = json.load(f)

with open(

    latest_run /

    "trend_report.json",

    "r",

    encoding="utf-8"

) as f:

    trends = json.load(f)

with open(

    latest_run /

    "update_impact_report.json",

    "r",

    encoding="utf-8"

) as f:

    update_impact = json.load(f)

executive_summary_path = (

    latest_run /

    "executive_summary.txt"
)

if executive_summary_path.exists():

    with open(

        executive_summary_path,

        "r",

        encoding="utf-8"

    ) as f:

        executive_summary = f.read()

else:

    executive_summary = ""

developer_report_path = (

    latest_run /

    "developer_report.txt"
)

if developer_report_path.exists():

    with open(

        developer_report_path,

        "r",

        encoding="utf-8"

    ) as f:

        developer_report = f.read()

else:

    developer_report = ""

ad_file = (

    latest_run /

    "ad_campaigns.txt"
)

with open(

    latest_run /

    "release_summary.json",

    "r",

    encoding="utf-8"

) as f:

    release_summary = json.load(f)

with open(

    latest_run /

    "ai_insights.txt",

    "r",

    encoding="utf-8"

) as f:

    ai_insights = f.read()

with open(

    latest_run /

    "review_impact_report.json",

    "r",

    encoding="utf-8"

) as f:

    review_impact = json.load(f)

if ad_file.exists():

    with open(

        ad_file,

        "r",

        encoding="utf-8"

    ) as f:

        ads = f.read()

else:

    ads = "No generated campaigns found."

metadata_path = (

    latest_run /

    "analysis_metadata.json"
)

if metadata_path.exists():

    with open(

        metadata_path,

        "r",

        encoding="utf-8"

    ) as f:

        run_metadata = json.load(f)

else:

    run_metadata = {}

with open(

    latest_run /

    "version_trend_report.json",

    "r",

    encoding="utf-8"

) as f:

    version_trends = json.load(f)

with open(

    latest_run /

    "marketing_confidence.json",

    "r",

    encoding="utf-8"

) as f:

    marketing_confidence = json.load(f)

segment_campaigns = (

    campaign_manager.load(

        latest_run
    )
)

segment_campaigns = (

    campaign_sync.sync(

        segment_campaigns
    )
)

metrics_df = (
    metrics_loader.load()
)

# st.write("Metrics CSV")
# st.dataframe(metrics_df)

segment_campaigns = (

    metrics_updater.update(

        segment_campaigns,

        metrics_df
    )
)

# st.write(
#     "Campaign Count:",
#     len(segment_campaigns)
# )

# st.write(
#     segment_campaigns
# )

with open(

    latest_run /

    "genre_profile.json",

    "r",

    encoding="utf-8"

) as f:

    genre_profile = json.load(f)

with open(

    latest_run /

    "campaign_plan.json",

    "r",

    encoding="utf-8"

) as f:

    campaign_plan = json.load(f)

pdf_path = (

    latest_run /

    "executive_report.pdf"
)

if pdf_path.exists():

    with open(

        pdf_path,

        "rb"

    ) as f:

        st.download_button(

            "📄 Download Executive Report",

            data=f,

            file_name=

            "executive_report.pdf",

            mime=

            "application/pdf"
        )

st.set_page_config(

    page_title="Game Intelligence",

    layout="wide"
)

st.title(
    f"🎮 {metadata['game_name']}"
)

st.sidebar.subheader(
    "Run Information"
)

st.sidebar.write(

    f"Game: "

    f"{run_metadata.get('game_name','-')}"
)

st.sidebar.write(

    f"Version: "

    f"{run_metadata.get('game_version','-')}"
)

st.sidebar.write(

    f"Reviews: "

    f"{run_metadata.get('review_count','-')}"
)

translator = (
    ReviewTranslator()
)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15, tab16 = st.tabs([

    "🎮 Game Intelligence",

    "📢 Marketing Intelligence",

    "🛠 Developer Report",

    "🚀 AI Campaigns",

    "📤 Campaign Approval",

    "📈 Trends",

    "📦 Update Impact",

    "⚙ Analysis Runner",

    "📊 Version Manager",

    "📋 Release Summary",

    "🧠 AI Insights",

    "🚀 Publishing Queue",

    "📊 Campaign Analytics",

    "💰 Sales",

    "💬 Sentiment",

    "🥊 Competitors"

])

with tab1:

    st.subheader(
        "Game Profile"
    )

    st.write(

        f"Genre: "

        f"{genre_profile['genre']}"
    )

    colA, colB= st.columns(2)

    colA.metric(

        "Reviews",

        metadata[
            "review_count"
        ]
    )

    # colB.metric(

    #     "Known Reviews",

    #     metadata[
    #         "known_reviews"
    #     ]
    # )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric(

        "Overall Health",

        health["overall_health"]
    )

    col2.metric(

        "Review Health",

        health["review_health"]
    )

    col3.metric(

        "Issue Health",

        health["issue_health"]
    )

    df = pd.DataFrame(
        issues
    )

    fig = px.bar(

        df,

        x="issue_id",

        y="count",

        title="Issue Distribution"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.subheader(
        "Top Issues"
    )

    st.dataframe(

        df[[
            "issue_id",
            "severity",
            "count",
            "impact_score",
            "helpful_count",
            "priority"
        ]],

        width="stretch"
    )

    st.divider()

    st.subheader(
        "Evidence Explorer"
    )

    selected_issue = st.selectbox(

        "Select Issue",

        df["issue_id"].tolist()
    )

    selected_row = (

        df[

            df["issue_id"]

            ==

            selected_issue

        ]

        .iloc[0]
    )


    severity = selected_row["severity"]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Severity",
        severity
    )

    col2.metric(
        "Mentions",
        selected_row["count"]
    )

    col3.metric(
        "Priority",
        selected_row["priority"]
    )

    st.write(
        f"Department: "
        f"{selected_row['department']}"
    )

    st.write(
        f"Team: "
        f"{selected_row['team']}"
    )

    top_reviews = (

        selected_row.get(

            "top_reviews",

            []
        )
    )

    st.subheader(

        "Top Evidence Reviews"
    )

    for idx, review in enumerate(

        top_reviews,

        start=1
    ):

        with st.container():

            st.markdown(
                f"### Evidence #{idx}"
            )

            evidence = review.get(

                "evidence",

                review["review_text"]
            )

            language = review.get(

                "language",

                "en"
            )

            if language == "en":

                display_text = evidence

            else:

                display_text = (

                    translator.translate(
                        evidence
                    )
                )

            st.markdown(
                f"> {display_text}"
            )
            
            st.caption(

                f"Impact: {review['impact_score']}"

                f" | Helpful: {review['helpful_count']}"
            )

            st.divider()

    st.subheader(
        "📋 Executive Summary"
    )

    st.text_area(

        "Executive Summary",

        executive_summary,

        height=300,

        label_visibility="collapsed"
    )

    # st.header(
    #     "📉 Review Impact Prediction"
    # )

    # impact_df = pd.DataFrame(
    #     review_impact
    # )

    # st.dataframe(

    #     impact_df,

    #     width="stretch"
    # )

with tab2:

    st.header(
        "📢 Marketing Intelligence"
    )

    col1, col2 = st.columns(2)

# Column 1: Target Audiences
    with col1:
        st.subheader("Target Audiences")
        for audience in marketing["target_audiences"]:
            st.write(f"• {audience}")

    # Column 2: Player Segments
    # with col2:
    #     st.subheader("Player Segments")
        
    #     segment_path = latest_run / "player_segment_report.txt"
    #     if segment_path.exists():
    #         with open(segment_path, "r", encoding="utf-8") as f:
    #             segment_report = f.read()
            
    #         # Using st.code to look clean and neat inside column layouts
    #         st.code(segment_report, language=None)

    # Full-width divider beneath both columns
    st.divider()

    st.subheader(
        "📈 Campaign Readiness"
    )

    col1, col2 = st.columns(2)

    col1.metric(

        "Campaign Score",

        campaigns[
            "campaign_score"
        ]
    )

    if campaigns["recommendation"] == "Launch":

        st.success(
            "✅ Launch Campaign"
        )

    else:

        st.warning(
            "⚠ Improve Game Before Campaign"
        )

    st.subheader(
        "Campaign Strategy"
    )

    st.write(
        "Recommended Channels"
    )

    for channel in campaign[
        "recommended_channels"
    ]:

        st.write(
            f"• {channel}"
        )

    st.write(
        "Promote"
    )

    for item in campaign[
        "promote"
    ]:

        st.write(
            f"• {item}"
        )

    st.write(
        "Avoid"
    )

    for item in campaign[
        "avoid"
    ]:

        st.write(
            f"• {item}"
        )

    st.divider()

    st.subheader("Marketing Angles")

    for angle in marketing["angles"]:
        st.write(f"• {angle}")

    st.header(
        "📢 Campaign Planner"
    )

    campaign_df = pd.DataFrame(
        campaign_plan
    )

    st.dataframe(

        campaign_df,

        width="stretch"
    )

    st.header(
        "📉 Revenue Risk Analysis"
    )

    impact_df = pd.DataFrame(
        review_impact
    )

    st.dataframe(

        impact_df.iloc[:, :-1],

        width="stretch"
    )

    # st.header(
    #     "🎯 Marketing Readiness"
    # )

    # col1, col2 = st.columns(2)

    # col1.metric(

    #     "Confidence Score",

    #     marketing_confidence[
    #         "marketing_confidence"
    #     ]
    # )

    # col2.metric(

    #     "Recommendation",

    #     marketing_confidence[
    #         "recommendation"
    #     ]
    # )

    st.header(
        "🎯 Segment Campaigns"
    )

    segment_df = pd.DataFrame(
        segment_campaigns
    )

    # st.write(segment_campaigns)

    for campaign in (

        segment_campaigns
    ):

        st.subheader(

            campaign[
                "audience"
            ]
        )

        st.write(

            f"Channel: "

            f"{campaign['channel']}"
        )

        st.markdown(

            f"### {campaign['headline']}"
        )

        st.write(

            campaign[
                "ad_copy"
            ]
        )

        st.success(

            campaign[
                "cta"
            ]
        )

        st.code(

            campaign[
                "tracking_url"
            ]
        )

        creatives = campaign.get(
            "creatives",
            {}
        )

        st.subheader(
            "Headline"
        )

        st.write(
            creatives.get(
                "headline",
                "Not Generated"
            )
        )

        platform = campaign.get(
            "platform",
            ""
        )

        if platform == "reddit":

            st.subheader(
                "Reddit Ad"
            )

        elif platform == "discord":

            st.subheader(
                "Discord Ad"
            )

        elif platform == "email":

            st.subheader(
                "Email Campaign"
            )

        else:

            st.subheader(
                "Ad Copy"
            )

        st.write(

            creatives.get(

                "ad_copy",

                "No ad copy generated."
            )
        )

        st.write(

            creatives.get(

                "ad_copy",

                "No ad copy generated."
            )
        )

        st.success(
            creatives.get(
                "cta",
                "Not Generated"
            )
        )

        st.divider()

with tab3:

    st.header(
        "🛠 Developer Report"
    )

    st.text_area(

        "Developer Report",

        developer_report,

        height=800,

        label_visibility="collapsed"
    )

with tab4:

    st.header(
        "🚀 Campaign Readiness"
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Campaign Score",
        campaigns["campaign_score"]
    )

    if campaigns["recommendation"] == "Launch":

        col2.success(
            "✅ Launch Campaign"
        )

    else:

        col2.warning(
            "⚠ Improve Before Launch"
        )

    st.divider()

    st.subheader(
        "Generated Campaigns"
    )

    st.text_area(

        "Ads",

        ads,

        height=400
    )

with tab5:

    st.header(
        "📤 Campaign Approval"
    )
    

    if len(segment_campaigns) == 0:

        st.warning(
            "No campaigns available."
        )

    else:

        pending_count = len([

            c

            for c in segment_campaigns

            if c.get(

                "status",

                "PENDING"

            ) == "PENDING"
        ])

        approved_count = len([

            c

            for c in segment_campaigns

            if c.get(

                "status",

                "PENDING"

            ) == "APPROVED"
        ])

        rejected_count = len([

            c

            for c in segment_campaigns

            if c.get(

                "status",

                "PENDING"

            ) == "REJECTED"
        ])

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Pending",
            pending_count
        )

        col2.metric(
            "Approved",
            approved_count
        )

        col3.metric(
            "Rejected",
            rejected_count
        )

        st.divider()

        for idx, campaign in enumerate(

            segment_campaigns
        ):

            audience = campaign.get(

                "audience",

                "Unknown Audience"
            )

            channel = campaign.get(

                "channel",

                "Unknown Channel"
            )

            status = campaign.get(

                "status",

                "PENDING"
            )

            creatives = campaign.get(

                "creatives",

                {}
            )

            st.subheader(
                audience
            )

            platform = campaign.get(

                "platform",

                "unknown"
            )

            st.write(

                f"Platform: {platform}"
            )

            st.write(

                f"Channel: {channel}"
            )

            if status == "APPROVED":

                st.success(
                    f"Status: {status}"
                )

            elif status == "REJECTED":

                st.error(
                    f"Status: {status}"
                )

            else:

                st.warning(
                    f"Status: {status}"
                )

            st.markdown(
                "### 📰 Headline"
            )

            st.info(

                creatives.get(

                    "headline",

                    "No headline generated."
                )
            )

            platform = campaign.get(

                "platform",

                ""
            )

            if platform == "reddit":

                st.markdown(
                    "### Reddit Ad"
                )

            elif platform == "discord":

                st.markdown(
                    "### Discord Ad"
                )

            elif platform == "email":

                st.markdown(
                    "### Email Campaign"
                )

            else:

                st.markdown(
                    "### Ad Copy"
                )

            st.write(

                creatives.get(

                    "ad_copy",

                    "No ad copy generated."
                )
            )

            st.markdown(
                "### CTA"
            )

            st.success(

                creatives.get(

                    "cta",

                    "Play Now"
                )
            )

            tracking_url = campaign.get(

                "tracked_url",

                campaign.get(

                    "tracking_url"
                )
            )

            if tracking_url:

                st.markdown(
                    "### Tracking URL"
                )

                st.code(
                    tracking_url
                )

            if status == "PENDING":

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(

                        "✅ Approve",

                        key=f"approve_{idx}"
                    ):
                        # st.write("BUTTON CLICKED")

                        segment_campaigns[idx][

                            "status"

                        ] = "APPROVED"

                        campaign_manager.save(

                            latest_run,

                            segment_campaigns
                        )

                        CampaignRepository().log_approval(

                            segment_campaigns[idx]["campaign_id"],

                            "APPROVED",

                            latest_run.name
                        )

                        # st.write(
                        #     segment_campaigns[idx]
                        # )

                        st.rerun()

                with col2:

                    if st.button(

                        "❌ Reject",

                        key=f"reject_{idx}"
                    ):

                        segment_campaigns[idx][

                            "status"

                        ] = "REJECTED"

                        campaign_manager.save(

                            latest_run,

                            segment_campaigns
                        )

                        CampaignRepository().log_approval(

                            segment_campaigns[idx]["campaign_id"],

                            "REJECTED",

                            latest_run.name
                        )

                        st.rerun()

            st.divider()

with tab6:

    st.header(
        "📈 Issue Trends"
    )

    if len(trends) == 0:

        st.warning(
            "No trend data available yet."
        )

    else:

        trend_options = list(
            trends.keys()
        )

        selected_issue = st.selectbox(

            "Select Issue",

            trend_options,

            key="trend_issue"
        )

        values = trends[
            selected_issue
        ]

        issue_data = trends[
            selected_issue
        ]

        trend_df = pd.DataFrame({

            "Run":
            list(
                issue_data.keys()
            ),

            "Mentions":
            list(
                issue_data.values()
            )
        })

        fig = px.line(

            trend_df,

            x="Run",

            y="Mentions",

            markers=True,

            title=f"{selected_issue} Trend"
        )

        st.plotly_chart(

            fig,

            width="stretch"
        )

        st.dataframe(

            trend_df,

            width="stretch"
        )

        trend_df = trend_df.sort_values(
            "Run"
        )

        latest = trend_df[
            "Mentions"
        ].iloc[-1]

        first = trend_df[
            "Mentions"
        ].iloc[0]

        change = latest - first

        st.metric(

            "Overall Change",

            latest,

            delta=change,

            delta_color="inverse"
        )

        st.divider()

    st.header(
        "🔥 Issue Heatmap"
    )

    heatmap_rows = []

    for issue, issue_data in (

        trends.items()
    ):

        row = {

            "Issue":
            issue
        }

        for run_name, count in (

            issue_data.items()
        ):

            row[
                run_name
            ] = count

        heatmap_rows.append(
            row
        )
        
    heatmap_df = pd.DataFrame(
        heatmap_rows
    )

    heatmap_chart_df = (

        heatmap_df

        .set_index(
            "Issue"
        )

        .fillna(0)
    )

    fig = px.imshow(

        heatmap_chart_df,

        aspect="auto",

        title="Issue Heatmap"
    )

    st.plotly_chart(

        fig,

        width="stretch"
    )

    st.header(
        "❤️ Health Trends"
    )

    health_df = pd.DataFrame(
        version_trends
    )

    fig = px.line(

        health_df,

        x="version",

        y="overall_health",

        markers=True,

        title="Overall Health Over Versions"
    )

    st.plotly_chart(

        fig,

        width="stretch"
    )

    fig = px.line(

        health_df,

        x="version",

        y="review_health",

        markers=True,

        title="Review Health Over Versions"
    )

    st.plotly_chart(

        fig,

        width="stretch"
    )

with tab7:

    st.header(
        "📦 Update Impact Analysis"
    )

    if len(update_impact) == 0:

        st.warning(
            "Need at least two runs."
        )

    else:

        comparison = update_impact.get(

            "_comparison",

            {}
        )

        if comparison:

            st.info(

                f"Comparing "

                f"{comparison['previous_version']} "

                f"({comparison['previous_period']}) "

                f"vs "

                f"{comparison['current_version']} "

                f"({comparison['current_period']})"
            )

        impact_rows = []

        for issue, data in (

            update_impact.items()
        ):

            if issue == "_comparison":

                continue

            impact_rows.append({

                "Issue":
                issue,

                "Before":
                data["before"],

                "After":
                data["after"],

                "Change %":
                data["change_percent"]
            })

        impact_df = pd.DataFrame(
            impact_rows
        )

        st.dataframe(

            impact_df,

            width="stretch"
        )

        improved = impact_df[

            impact_df["Change %"] < 0
        ]

        worsened = impact_df[

            impact_df["Change %"] > 0
        ]

        st.subheader(
            "Improved Issues"
        )

        for _, row in improved.iterrows():

            st.success(

                f"{row['Issue']} "

                f"({row['Change %']}%)"
            )

        st.subheader(
            "Worsened Issues"
        )

        for _, row in worsened.iterrows():

            st.error(

                f"{row['Issue']} "

                f"(+{row['Change %']}%)"
            )

        top_improved = (

            impact_df

            .sort_values(

                "Change %"
            )

            .head(3)
        )
                
        st.subheader(
            "Patch Impact Summary"
        )

        for _, row in top_improved.iterrows():

            st.write(

                f"✅ {row['Issue']} "

                f"improved by "

                f"{abs(row['Change %'])}%"
            )

with tab8:

    st.header(
        "Analysis Configuration"
    )

    game_name = st.text_input(
        "Game Name"
    )

    app_id = st.text_input(
        "App ID"
    )

    version = st.text_input(
        "Version"
    )

    start_date = st.date_input(
        "Review Start Date"
    )

    end_date = st.date_input(
        "Review End Date"
    )

    if st.button(

        "Save Configuration"
    ):
        
            config = {

                "game_name":
                game_name,

                "app_id":
                app_id,

                "game_version":
                version,

                "review_start_date":
                str(start_date),

                "review_end_date":
                str(end_date)
            }

            with open(

                "config/analysis_config.json",

                "w",

                encoding="utf-8"

            ) as f:

                json.dump(

                    config,

                    f,

                    indent=4
                )

            st.success(
                "Configuration Saved"
            )

    if st.button(
        "Run Analysis"
    ):

        with st.spinner(

            "Running analysis..."
        ):

            subprocess.run(

                [

                    sys.executable,

                    "-m",

                    "pipeline.run_full_analysis"
                ]
            )

        st.success(

            "Analysis Complete"
        )

    st.divider()

    st.subheader(
        "Full Pipeline (Steam App ID)"
    )

    st.caption(
        "Scrape → preprocess → Ollama insights → analysis → "
        "Gemini ads → distribution preview (dry-run, nothing is sent)"
    )

    pipeline_app_id = st.text_input(

        "Steam App ID",

        value=app_id or "3297310",

        key="pipeline_app_id"
    )

    pipeline_max_reviews = st.number_input(

        "Max reviews",

        min_value=10,

        max_value=500,

        value=200,

        step=10
    )

    if st.button(
        "Run Full Pipeline"
    ):

        with st.spinner(

            "Running full pipeline (this can take a while)..."
        ):

            result = subprocess.run(

                [

                    sys.executable,

                    "run_pipeline.py",

                    "--app-id",

                    str(pipeline_app_id),

                    "--max-reviews",

                    str(int(pipeline_max_reviews))
                ],

                capture_output=True,

                text=True,

                encoding="utf-8",

                errors="replace",

                env={

                    **os.environ,

                    "PYTHONIOENCODING": "utf-8"
                }
            )

        if result.returncode == 0:

            st.success(
                "Pipeline complete. Pick the newest run in the sidebar."
            )

        else:

            st.error(
                "Pipeline failed"
            )

        st.code(

            (result.stdout + result.stderr)[-5000:]
        )

with tab9:

    st.header(
        "📊 Version Manager"
    )

    version_df = pd.DataFrame(

        all_versions
    )

    st.dataframe(

        version_df,

        width="stretch"
    )

    games = sorted(

        version_df[
            "game_name"
        ].unique()
    )

    selected_game = st.selectbox(

        "Select Game",

        games
    )

    filtered_versions = (

        version_df[

            version_df[
                "game_name"
            ]

            ==

            selected_game
        ]
    )

    st.subheader(
        "Game Versions"
    )

    st.dataframe(

        filtered_versions,

        width="stretch"
    )

    versions = (

        filtered_versions[
            "game_version"
        ]

        .tolist()
    )

    col1, col2 = st.columns(2)

    version_a = col1.selectbox(

        "Version A",

        versions,

        key="version_a"
    )

    version_b = col2.selectbox(

        "Version B",

        versions,

        key="version_b"
    )

    compare_clicked = st.button(
        "Compare Versions"
    )

    if compare_clicked:

        run_a = filtered_versions[
            filtered_versions[
                "game_version"
            ] == version_a
        ].iloc[0]

        run_b = filtered_versions[
            filtered_versions[
                "game_version"
            ] == version_b
        ].iloc[0]


        with open(

            Path("outputs") /
            run_a["run"] /
            "issues.json",

            "r",

            encoding="utf-8"

        ) as f:

            issues_a = json.load(f)

        with open(

            Path("outputs") /
            run_b["run"] /
            "issues.json",

            "r",

            encoding="utf-8"

        ) as f:

            issues_b = json.load(f)

        map_a = {

            issue["issue_id"]:
            issue["count"]

            for issue in issues_a
        }

        map_b = {

            issue["issue_id"]:
            issue["count"]

            for issue in issues_b
        }

        all_issues = (

            set(map_a.keys())

            |

            set(map_b.keys())
        )

        comparison_rows = []

        for issue in all_issues:

            before = map_a.get(
                issue,
                0
            )

            after = map_b.get(
                issue,
                0
            )

            if before == 0:

                change = 100

            else:

                change = round(

                    (
                        after - before
                    )

                    /

                    before

                    * 100,

                    1
                )

            comparison_rows.append({

                "Issue":
                issue,

                version_a:
                before,

                version_b:
                after,

                "Change %":
                change
            })

        comparison_df = pd.DataFrame(
            comparison_rows
        )

        comparison_df = (

            comparison_df

            .sort_values(

                "Change %"
            )
        )

        st.subheader(
            f"{version_a} vs {version_b}"
        )

        st.dataframe(

            comparison_df,

            width="stretch"
        )

with tab10:
    st.header(
        "📋 Release Summary"
    )

    st.metric(

        "Overall Health",

        release_summary[
            "overall_health"
        ]
    )

    st.subheader(
        "Target Audiences"
    )

    for audience in (

        release_summary[
            "target_audiences"
        ]
    ):

        st.write(
            f"• {audience}"
        )

    st.subheader(
        "Top Improvements"
    )

    for item in (

        release_summary[
            "top_improvements"
        ]
    ):

        st.success(

            f"{item['issue']} "

            f"{item['change']}%"
        )

    st.subheader(
        "Top Regressions"
    )

    for item in (

        release_summary[
            "top_regressions"
        ]
    ):

        st.error(

            f"{item['issue']} "

            f"+{item['change']}%"
        )

with tab11:

    st.header(
        "🧠 AI Executive Insights"
    )

    st.text_area(

        "AI Insights",

        ai_insights,

        height=700,

        label_visibility="collapsed"
    )

with tab12:

    st.header(
        "Publishing Queue"
    )

    live_mode = st.toggle(

        "Live mode (actually send)",

        value=False,

        help="Off = dry-run: shows what would be sent, sends nothing."
    )

    if live_mode:

        st.warning(
            "LIVE: Publish posts to Discord / Reddit / Email for real."
        )

    else:

        st.info(
            "Dry-run: Publish previews the message only."
        )

    approved_campaigns = (

        publishing_queue.get_ready_campaigns(

            segment_campaigns
        )
    )

    if approved_campaigns and st.button(

        "Distribute all approved"

        + (" (LIVE)" if live_mode else " (dry-run)")
    ):

        for campaign in approved_campaigns:

            if campaign.get("status") != "APPROVED":

                continue

            result = publisher.publish(

                campaign,

                dry_run=not live_mode
            )

            if live_mode and result:

                campaign["status"] = "PUBLISHED"

                campaign["published_at"] = (
                    datetime.now().isoformat()
                )

            st.write(

                f"{campaign['campaign_id']}: "

                + ("sent" if live_mode and result else "previewed")
            )

            if not live_mode:

                st.json(

                    result

                    if isinstance(result, dict)

                    else campaign.get("creatives", {})
                )

        if live_mode:

            campaign_manager.save(
                latest_run,
                segment_campaigns
            )
    if not approved_campaigns:

        st.info(

            "No approved campaigns."
        )

    for idx, campaign in enumerate(
        approved_campaigns
    ):
        
        st.caption(

            f"Platform: "

            f"{campaign['platform']}"
        )

        st.subheader(

            campaign["audience"]
        )

        st.write(

            f"Channel: "

            f"{campaign['channel']}"
        )

        creatives = campaign.get(

            "creatives",

            {}
        )

        st.markdown(
            "### 📰 Headline"
        )

        st.info(

            creatives.get(

                "headline",

                "No headline"
            )
        )

        st.markdown(
            "### 📢 Ad Copy"
        )

        st.write(

            creatives.get(

                "ad_copy",

                "No ad copy"
            )
        )

        st.markdown(
            "### 🎯 CTA"
        )

        st.write(

            creatives.get(

                "cta",

                "Play Now"
            )
        )

        if campaign["status"] == "PUBLISHED":

            st.write(
                "STATUS: Published from Approved"
            )

        elif campaign["status"] == "APPROVED":

            st.info(
                "APPROVED"
            )

        else:

            st.warning(
                campaign["status"]
            )

        if campaign.get(
            "published_at"
        ):
            st.caption(
                f"Published: "
                f"{campaign['published_at']}"
            )

        st.code(

            campaign.get(

                "tracked_url",

                ""
            )
        )

        path = Path(

            "data/campaign_links.json"
        )

        if path.exists():

            with open(

                path,

                "r",

                encoding="utf-8"

            ) as f:

                links = json.load(f)

            short_code = campaign.get(

                "short_code"
            )

            if short_code in links:

                st.metric(

                    "Clicks",

                    links[short_code][

                        "clicks"
                    ]
                )


        if campaign.get(

            "status"

        ) == "APPROVED":

            if st.button(

                "Publish",

                key=f"publish_{idx}"
            ):

                success = (

                    publisher.publish(

                        campaign,

                        dry_run=not live_mode
                    )
                )

                if success and not live_mode:

                    st.info(
                        "Dry-run: nothing was sent."
                    )

                    st.json(

                        success

                        if isinstance(success, dict)

                        else campaign.get("creatives", {})
                    )

                elif success:

                    campaign["status"] = (

                        "PUBLISHED"
                    )

                    campaign["published_at"] = (

                        datetime.now()

                        .isoformat()
                    )

                    campaign_manager.save(

                        latest_run,

                        segment_campaigns
                    )

                    st.success(

                        "Published"
                    )

                    if campaign.get(

                        "published_at"
                    ):
                        st.caption(

                            f"Published: "

                            f"{campaign['published_at']}"
                        )

                    st.rerun()

                else:

                    st.error(

                        "Publishing failed"
                    )
        else: 
            st.success(

                campaign["status"]
            )


        st.divider()

    st.subheader(
        "Publishing Logs"
    )

    log_file = Path(
        "outputs/publishing_logs.json"
    )

    if log_file.exists():

        with open(

            log_file,

            "r",

            encoding="utf-8"

        ) as f:

            logs = json.load(f)

        if logs:

            log_df = pd.DataFrame(

                logs[::-1]
            )

            st.dataframe(

                log_df,

                width="stretch"
            )

        else:

            st.info(
                "No logs yet."
            )

    else:

        st.info(
            "No publishing logs found."
        )

    if log_file.exists():

        total_logs = len(logs)

        success_logs = len([

            x

            for x in logs

            if x["status"]

            ==

            "SUCCESS"
        ])

        failed_logs = len([

            x

            for x in logs

            if x["status"]

            ==

            "FAILED"
        ])

        success_rate = 0

        if total_logs > 0:

            success_rate = round(

                success_logs

                /

                total_logs

                * 100,

                1
            )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(

            "Total Publishes",

            total_logs
        )

        col2.metric(

            "Successful",

            success_logs
        )

        col3.metric(

            "Failed",

            failed_logs
        )

        col4.metric(

            "Success Rate",

            f"{success_rate}%"
        ) 

    st.divider()

    st.subheader(
        "Campaign History"
    )

    if log_file.exists():

        history = {}

        for log in logs:

            campaign_id = log[
                "campaign_id"
            ]

            history[
                campaign_id
            ] = log[
                "status"
            ]

        history_df = pd.DataFrame([

            {

                "campaign_id":
                k,

                "publish_result":
                v

            }

            for k, v

            in history.items()
        ])

        st.dataframe(

            history_df,

            width="stretch"
        )

    st.divider()

    st.subheader(
        "Top Campaigns"
    )
    leaderboard = []

    for campaign in segment_campaigns:

        leaderboard.append({

            "audience":
            campaign["audience"],

            "status":
            campaign["status"],

            "clicks":
            campaign.get(
                "clicks",
                0
            )
        })

    leaderboard_df = pd.DataFrame(
        leaderboard
    )

    leaderboard_df = (

        leaderboard_df

        .sort_values(

            "clicks",

            ascending=False
        )
    )

    st.dataframe(

        leaderboard_df,

        width="stretch"
    )
    
    st.divider()

    st.subheader(
        "Publishing Insights"
    )

    insights = (

        publishing_analytics.analyze(

            segment_campaigns
        )
    )

    if insights:

        col1, col2 = st.columns(2)

        col1.metric(

            "Best Audience",

            insights[
                "best_audience"
            ]
        )

        col2.metric(

            "Best Channel",

            insights[
                "best_channel"
            ]
        )

    worst = insights.get(

        "worst_campaign",

        {}
    )

    if worst:

        st.warning(

            f"""
    Audience:
    {worst.get('audience','Unknown')}

    Platform:
    {worst.get('platform','Unknown')}

    Clicks:
    {worst.get('clicks',0)}

    Status:
    {worst.get('status','Unknown')}
    """
        )

    st.divider()

    # st.subheader(
    #     "Reddit Drafts"
    # )

    # reddit_campaigns = [

    #     c

    #     for c

    #     in segment_campaigns

    #     if c.get(

    #         "platform"

    #     ) == "reddit"
    # ]

    # for idx, campaign in enumerate(
    #     reddit_campaigns
    # ):
    #     st.subheader(

    #         campaign["audience"]
    #     )

    #     st.caption(

    #         f"Campaign ID: "

    #         f"{campaign['campaign_id']}"
    #     )

    #     creatives = campaign.get(

    #         "creatives",

    #         {}
    #     )

    #     st.text_area(

    #         "Title",

    #         creatives.get(

    #             "headline",

    #             ""
    #         ),

    #         disabled=True,

    #         key=f"title_{idx}"
    #     )

    #     st.text_area(

    #         "Body",

    #         creatives.get(

    #             "ad_copy",

    #             ""
    #         ),

    #         height=200,

    #         disabled=True,

    #         key=f"body_{idx}"
    #     )

    # st.divider()

    # st.subheader(
    #     "Email Drafts"
    # )

    # email_campaigns = [

    #     c

    #     for c

    #     in segment_campaigns

    #     if c.get(

    #         "platform"

    #     ) == "email"
    # ]

    # for idx, campaign in enumerate(
    #     email_campaigns
    # ):

    #     creatives = campaign.get(

    #         "creatives",

    #         {}
    #     )

    #     st.subheader(

    #         campaign["audience"]
    #     )

    #     st.text_area(

    #         "Email Headline",

    #         creatives.get(

    #             "headline",

    #             ""
    #         ),

    #         disabled=True,

    #         key=f"email_title_{idx}"
    #     )

    #     st.text_area(

    #         "Email Body",

    #         creatives.get(

    #             "ad_copy",

    #             ""
    #         ),

    #         height=250,

    #         disabled=True,

    #         key=f"email_body_{idx}"
    #     )

    # st.divider()

    # st.subheader(
    #     "Discord Drafts"
    # )

    # discord_campaigns = [

    #     c

    #     for c

    #     in segment_campaigns

    #     if c.get(

    #         "platform"

    #     ) == "discord"
    # ]

    # for idx, campaign in enumerate(
    #     discord_campaigns
    # ):

    #     creatives = campaign.get(

    #         "creatives",

    #         {}
    #     )

    #     st.subheader(

    #         campaign["audience"]
    #     )

    #     st.text_area(

    #         "Discord Message",

    #         creatives.get(

    #             "ad_copy",

    #             ""
    #         ),

    #         height=150,

    #         disabled=True,

    #         key=f"discord_body_{idx}"
    #     )
    

    

with tab13:
    st.header(

        "Campaign Analytics"
    )

    analytics = (

        campaign_analytics.analyze(

            segment_campaigns
        )
    )
    analytics_df = pd.DataFrame(
        analytics
    )

    required_cols = [

        "audience",

        "channel",

        "status",

        "impressions",

        "clicks",

        "visits",

        "wishlists",

        "downloads",

        "ctr",

        "wishlist_rate",

        "download_rate"
    ]

    for col in required_cols:

        if col not in analytics_df.columns:

            analytics_df[col] = 0

    analytics_view = analytics_df[
        required_cols
    ]

    st.dataframe(

        analytics_view,

        width="stretch"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(

        "Total Clicks",

        analytics_df[
            "clicks"
        ].sum()
    )

    col2.metric(

        "Total Wishlists",

        analytics_df[
            "wishlists"
        ].sum()
    )

    col3.metric(

        "Total Downloads",

        analytics_df[
            "downloads"
        ].sum()
    )

    # st.write(
    #     analytics_df.columns.tolist()
    # )


from services.steam_market import (
    SteamMarket,
    DEFAULT_COMPETITORS
)


def load_run_json(name):

    path = latest_run / name

    if not path.exists():

        return None

    with open(

        path,

        "r",

        encoding="utf-8"

    ) as f:

        return json.load(f)


def load_market_report():

    # Prefer this run's snapshot; fall back to the cached
    # Steam/SteamSpy data so the views render offline.

    report = load_run_json(
        "market_report.json"
    )

    if report:

        return report, "run"

    cache_path = Path(
        "data/market_cache.json"
    )

    if not cache_path.exists():

        return None, None

    with open(

        cache_path,

        "r",

        encoding="utf-8"

    ) as f:

        cache = json.load(f)

    with open(

        "config/analysis_config.json",

        "r",

        encoding="utf-8"

    ) as f:

        current_app = str(
            json.load(f).get("app_id", "")
        )

    if current_app not in cache:

        return None, None

    return {

        "game":
        cache[current_app],

        "competitors": [

            snap

            for key, snap in cache.items()

            if key != current_app
        ]
    }, "cache"


market_report, market_source = (
    load_market_report()
)

insights = load_run_json(
    "insights.json"
)

with tab14:

    st.header(
        "Sales"
    )

    st.caption(
        "Steam does not publish sales. Owners are SteamSpy's estimate range; "
        "revenue = owners midpoint × current US price (before Steam's cut, "
        "ignores discounts and regional pricing)."
    )

    if not market_report:

        st.info(
            "No market data yet. Run the full pipeline from the Analysis Runner tab."
        )

    else:

        if market_source == "cache":

            st.warning(
                "Showing cached market data (this run has no market_report.json)."
            )

        game = market_report["game"]

        st.subheader(
            game.get("name", f"App {game.get('app_id')}")
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(

            "Price (USD)",

            "Free" if game.get("is_free") else f"${game.get('price_usd', 0):.2f}"
        )

        col2.metric(

            "Estimated Owners",

            f"{game.get('owners_estimate', 0):,}"
        )

        col3.metric(

            "Estimated Revenue",

            f"${game.get('revenue_estimate_usd', 0):,.0f}"
        )

        col4.metric(

            "Concurrent Players",

            f"{game.get('ccu', 0):,}"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(

            "Steam Reviews",

            f"{game.get('total_reviews', 0):,}"
        )

        col2.metric(

            "Positive",

            f"{game.get('positive_ratio', 0)}%"
        )

        col3.metric(

            "Avg Playtime (h)",

            game.get("average_playtime_hours", 0)
        )

        st.write(

            f"Owners range: {game.get('owners', '-')} | "

            f"Released: {game.get('release_date', '-')} | "

            f"Fetched: {game.get('fetched_at', '-')}"
        )

    st.subheader(
        "Campaign Funnel"
    )

    if not metrics_df.empty:

        funnel = (

            metrics_df

            .groupby("date")[

                ["clicks", "visits", "wishlists", "downloads"]
            ]

            .sum()

            .reset_index()
        )

        st.plotly_chart(

            px.line(

                funnel,

                x="date",

                y=["clicks", "visits", "wishlists", "downloads"],

                markers=True
            ),

            width="stretch"
        )

    else:

        st.info(
            "No outputs/campaign_metrics.csv data."
        )

with tab15:

    st.header(
        "Player Sentiment"
    )

    if insights:

        st.caption(

            f"Ollama analysis of {insights['count']} reviews"
        )

        col1, col2 = st.columns(2)

        sentiment_df = pd.DataFrame(

            list(insights["sentiment"].items()),

            columns=["sentiment", "reviews"]
        )

        col1.plotly_chart(

            px.pie(

                sentiment_df,

                names="sentiment",

                values="reviews",

                title="Sentiment"
            ),

            width="stretch"
        )

        emotion_df = pd.DataFrame(

            list(insights.get("emotion_counts", {}).items()),

            columns=["emotion", "mentions"]
        )

        if not emotion_df.empty:

            col2.plotly_chart(

                px.bar(

                    emotion_df,

                    x="emotion",

                    y="mentions",

                    title="Emotions"
                ),

                width="stretch"
            )

        topic_df = pd.DataFrame(

            list(insights.get("topic_counts", {}).items()),

            columns=["topic", "mentions"]
        )

        if not topic_df.empty:

            st.plotly_chart(

                px.bar(

                    topic_df.sort_values("mentions"),

                    x="mentions",

                    y="topic",

                    orientation="h",

                    title="Topics"
                ),

                width="stretch"
            )

        st.subheader(
            "Player Segments"
        )

        segment_rows = []

        for name, seg in insights.get("segments", {}).items():

            total = max(seg["count"], 1)

            segment_rows.append({

                "segment":
                name,

                "reviews":
                seg["count"],

                "positive %":
                round(seg["sentiment"].get("positive", 0) / total * 100, 1),

                "negative %":
                round(seg["sentiment"].get("negative", 0) / total * 100, 1),

                "top emotions":
                ", ".join(seg["top_emotions"]),

                "top topics":
                ", ".join(seg["top_topics"])
            })

        st.dataframe(

            pd.DataFrame(segment_rows),

            width="stretch"
        )

    else:

        st.warning(
            "This run has no Ollama insights.json; showing recommendation "
            "split from data/language_reviews.csv instead."
        )

        reviews_path = Path(
            "data/language_reviews.csv"
        )

        if reviews_path.exists():

            reviews_df = pd.read_csv(
                reviews_path
            )

            split = (

                reviews_df["is_positive"]

                .map({True: "positive", False: "negative"})

                .value_counts()

                .reset_index()
            )

            split.columns = [
                "sentiment",
                "reviews"
            ]

            st.plotly_chart(

                px.pie(

                    split,

                    names="sentiment",

                    values="reviews"
                ),

                width="stretch"
            )

            if "player_segment" in reviews_df.columns:

                st.dataframe(

                    pd.crosstab(

                        reviews_df["player_segment"],

                        reviews_df["is_positive"]
                    ),

                    width="stretch"
                )

with tab16:

    st.header(
        "Competitor Analysis"
    )

    competitor_input = st.text_input(

        "Competitor App IDs (comma separated)",

        value=", ".join(

            str(c.get("app_id"))

            for c in (market_report or {}).get("competitors", [])

        ) or ", ".join(str(c) for c in DEFAULT_COMPETITORS)
    )

    if market_report and st.button(
        "Refresh from Steam"
    ):

        with st.spinner(
            "Fetching Steam + SteamSpy..."
        ):

            market_report = SteamMarket().build_report(

                market_report["game"]["app_id"],

                [

                    int(c)

                    for c in competitor_input.split(",")

                    if c.strip().isdigit()
                ]
            )

    if not market_report:

        st.info(
            "No market data yet. Run the full pipeline from the Analysis Runner tab."
        )

    else:

        rows = []

        for snap in [market_report["game"]] + market_report["competitors"]:

            rows.append({

                "game":
                snap.get("name", snap.get("app_id")),

                "app_id":
                snap.get("app_id"),

                "genres":
                ", ".join(snap.get("genres", [])),

                "price_usd":
                snap.get("price_usd", 0),

                "owners_estimate":
                snap.get("owners_estimate", 0),

                "revenue_estimate_usd":
                snap.get("revenue_estimate_usd", 0),

                "total_reviews":
                snap.get("total_reviews", 0),

                "positive_ratio":
                snap.get("positive_ratio", 0),

                "ccu":
                snap.get("ccu", 0)
            })

        comp_df = pd.DataFrame(rows)

        st.dataframe(

            comp_df,

            width="stretch"
        )

        col1, col2 = st.columns(2)

        col1.plotly_chart(

            px.bar(

                comp_df,

                x="game",

                y="positive_ratio",

                title="Positive Review %"
            ),

            width="stretch"
        )

        col2.plotly_chart(

            px.bar(

                comp_df,

                x="game",

                y="owners_estimate",

                title="Estimated Owners",

                log_y=True
            ),

            width="stretch"
        )

        st.plotly_chart(

            px.scatter(

                comp_df,

                x="price_usd",

                y="positive_ratio",

                size=comp_df["total_reviews"].clip(lower=1),

                hover_name="game",

                title="Price vs Reception (bubble = review count)"
            ),

            width="stretch"
        )
