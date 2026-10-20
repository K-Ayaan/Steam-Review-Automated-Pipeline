import json
import os
from pathlib import Path

try:

    import psycopg

    from psycopg.types.json import Jsonb

except ImportError:

    psycopg = None


# Status of the newest run that contains a campaign_id;
# approvals and publishes always act on the latest copy.

LATEST_CAMPAIGN = """
    UPDATE campaigns SET status = %s, updated_at = now(){published}
    WHERE campaign_id = %s
      AND run_id = COALESCE(%s, (
          SELECT max(run_id) FROM campaigns WHERE campaign_id = %s
      ))
"""


def read_json(

    path,

    default
):

    if not path.exists():

        return default

    with open(

        path,

        "r",

        encoding="utf-8"

    ) as f:

        return json.load(f)


class CampaignRepository:

    # Mirrors pipeline output into PostgreSQL.
    # JSON files stay the source of truth: without DATABASE_URL,
    # or with Postgres down, every method is a quiet no-op.

    def __init__(

        self,

        dsn=None
    ):

        self.dsn = (

            dsn

            or

            os.getenv(
                "DATABASE_URL"
            )
        )

    def connect(self):

        if not self.dsn or psycopg is None:

            return None

        try:

            return psycopg.connect(

                self.dsn,

                connect_timeout=3
            )

        except psycopg.Error as e:

            # Never print the DSN: it holds the password.

            print(
                f"[DB] Postgres unavailable, skipping mirror ({type(e).__name__})"
            )

            return None

    def execute(

        self,

        statements
    ):

        conn = self.connect()

        if conn is None:

            return False

        try:

            with conn:

                with conn.cursor() as cur:

                    for sql, params in statements:

                        cur.execute(
                            sql,
                            params
                        )

            return True

        except psycopg.Error as e:

            print(
                f"[DB] Mirror write failed: {type(e).__name__}: "
                f"{(str(e).splitlines() or [''])[0]}"
            )

            return False

    def save_run(

        self,

        run_dir,

        app_id,

        market=None
    ):

        run_dir = Path(run_dir)

        run_id = run_dir.name

        metadata = read_json(
            run_dir / "analysis_metadata.json",
            {}
        )

        insights = read_json(
            run_dir / "insights.json",
            {}
        )

        issues = read_json(
            run_dir / "issues.json",
            []
        )

        campaigns = read_json(
            run_dir / "segment_campaigns.json",
            []
        )

        market = market or read_json(
            run_dir / "market_report.json",
            {}
        )

        game = market.get(
            "game",
            {}
        )

        game_name = (

            metadata.get("game_name")

            or

            game.get("name")

            or

            str(app_id)
        )

        statements = [(

            """
            INSERT INTO games (app_id, name, genres, price_usd, market)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (app_id) DO UPDATE SET
                name = EXCLUDED.name,
                genres = EXCLUDED.genres,
                price_usd = EXCLUDED.price_usd,
                market = EXCLUDED.market,
                updated_at = now()
            """,

            (
                int(app_id),
                game_name,
                Jsonb(game.get("genres", [])),
                game.get("price_usd"),
                Jsonb(market)
            )
        ), (

            """
            INSERT INTO runs (run_id, app_id, game_name, analysis_date,
                              review_start, review_end, game_version,
                              review_count, insights)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (run_id) DO UPDATE SET
                insights = EXCLUDED.insights,
                review_count = EXCLUDED.review_count
            """,

            (
                run_id,
                int(app_id),
                game_name,
                metadata.get("analysis_date"),
                metadata.get("review_start_date"),
                metadata.get("review_end_date"),
                metadata.get("game_version"),
                metadata.get("review_count"),
                Jsonb(insights)
            )
        )]

        for issue in issues:

            statements.append((

                """
                INSERT INTO issues (run_id, issue_id, severity, priority,
                                    category, department, team,
                                    review_count, impact_score,
                                    ranking_score, data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (run_id, issue_id) DO UPDATE SET
                    data = EXCLUDED.data
                """,

                (
                    run_id,
                    issue.get("issue_id"),
                    issue.get("severity"),
                    issue.get("priority"),
                    issue.get("category"),
                    issue.get("department"),
                    issue.get("team"),
                    issue.get("count"),
                    issue.get("impact_score"),
                    issue.get("ranking_score"),
                    Jsonb(issue)
                )
            ))

        for campaign in campaigns:

            campaign_id = campaign.get(
                "campaign_id"
            )

            statements.append((

                """
                INSERT INTO campaigns (run_id, campaign_id, audience,
                                       platform, channel, status,
                                       generated_by, headline, ad_copy,
                                       cta, tracking_url, creatives,
                                       published_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (run_id, campaign_id) DO UPDATE SET
                    status = EXCLUDED.status,
                    creatives = EXCLUDED.creatives,
                    published_at = EXCLUDED.published_at,
                    updated_at = now()
                """,

                (
                    run_id,
                    campaign_id,
                    campaign.get("audience"),
                    campaign.get("platform"),
                    campaign.get("channel"),
                    campaign.get("status", "PENDING"),
                    campaign.get("generated_by"),
                    campaign.get("headline"),
                    campaign.get("ad_copy"),
                    campaign.get("cta"),
                    campaign.get("tracking_url"),
                    Jsonb(campaign.get("creatives", {})),
                    campaign.get("published_at")
                )
            ))

            statements.append((

                """
                INSERT INTO campaign_metrics (run_id, campaign_id, channel,
                                              impressions, clicks, visits,
                                              wishlists, downloads, spend)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (run_id, campaign_id) DO UPDATE SET
                    impressions = EXCLUDED.impressions,
                    clicks = EXCLUDED.clicks,
                    visits = EXCLUDED.visits,
                    wishlists = EXCLUDED.wishlists,
                    downloads = EXCLUDED.downloads,
                    spend = EXCLUDED.spend
                """,

                (
                    run_id,
                    campaign_id,
                    campaign.get("platform"),
                    campaign.get("impressions", 0),
                    campaign.get("clicks", 0),
                    campaign.get("visits", 0),
                    campaign.get("wishlists", 0),
                    campaign.get("downloads", 0),
                    campaign.get("spend", 0)
                )
            ))

            if campaign.get("short_code"):

                statements.append((

                    """
                    INSERT INTO campaign_links (short_code, run_id,
                                                campaign_id,
                                                destination_url,
                                                tracked_url)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (short_code) DO NOTHING
                    """,

                    (
                        campaign["short_code"],
                        run_id,
                        campaign_id,
                        campaign.get("tracking_url", ""),
                        campaign.get("tracked_url")
                    )
                ))

        if not self.execute(statements):

            return None

        counts = {

            "run_id": run_id,

            "issues": len(issues),

            "campaigns": len(campaigns)
        }

        print(
            f"[DB] Mirrored {run_id}: {counts['issues']} issues, "
            f"{counts['campaigns']} campaigns"
        )

        return counts

    def log_approval(

        self,

        campaign_id,

        status,

        run_id=None
    ):

        return self.execute([(

            """
            INSERT INTO approval_logs (run_id, campaign_id, status)
            VALUES (%s, %s, %s)
            """,

            (run_id, campaign_id, status)
        ), (

            LATEST_CAMPAIGN.format(published=""),

            (status, campaign_id, run_id, campaign_id)
        )])

    def log_publish(

        self,

        campaign_id,

        channel,

        status,

        message=""
    ):

        statements = [(

            """
            INSERT INTO publishing_logs (campaign_id, channel, status, message)
            VALUES (%s, %s, %s, %s)
            """,

            (campaign_id, channel, status, message)
        )]

        if status == "SUCCESS":

            statements.append((

                LATEST_CAMPAIGN.format(
                    published=", published_at = now()"
                ),

                ("PUBLISHED", campaign_id, None, campaign_id)
            ))

        return self.execute(
            statements
        )
