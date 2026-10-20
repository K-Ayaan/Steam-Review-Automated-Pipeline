-- PostgreSQL mirror of the pipeline's JSON output.
-- Loaded automatically by docker compose on the first start
-- (an empty postgres_data volume). JSON files stay the source of truth.

CREATE TABLE IF NOT EXISTS games (
    app_id          BIGINT PRIMARY KEY,
    name            TEXT NOT NULL,
    genres          JSONB NOT NULL DEFAULT '[]',
    price_usd       NUMERIC(10, 2),
    market          JSONB NOT NULL DEFAULT '{}',
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS runs (
    run_id          TEXT PRIMARY KEY,               -- outputs/run_<timestamp> folder name
    app_id          BIGINT REFERENCES games (app_id),
    game_name       TEXT,
    analysis_date   DATE,
    review_start    TIMESTAMP,
    review_end      TIMESTAMP,
    game_version    TEXT,
    review_count    INTEGER,
    insights        JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS issues (
    run_id          TEXT NOT NULL REFERENCES runs (run_id) ON DELETE CASCADE,
    issue_id        TEXT NOT NULL,
    severity        TEXT,
    priority        TEXT,
    category        TEXT,
    department      TEXT,
    team            TEXT,
    review_count    INTEGER,
    impact_score    NUMERIC,
    ranking_score   NUMERIC,
    data            JSONB NOT NULL DEFAULT '{}',
    PRIMARY KEY (run_id, issue_id)
);

CREATE TABLE IF NOT EXISTS campaigns (
    run_id          TEXT NOT NULL REFERENCES runs (run_id) ON DELETE CASCADE,
    campaign_id     TEXT NOT NULL,
    audience        TEXT,
    platform        TEXT,
    channel         TEXT,
    status          TEXT NOT NULL DEFAULT 'PENDING',
    generated_by    TEXT,
    headline        TEXT,
    ad_copy         TEXT,
    cta             TEXT,
    tracking_url    TEXT,
    creatives       JSONB NOT NULL DEFAULT '{}',
    published_at    TIMESTAMPTZ,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (run_id, campaign_id)
);

CREATE INDEX IF NOT EXISTS campaigns_campaign_id_idx ON campaigns (campaign_id);

CREATE TABLE IF NOT EXISTS campaign_links (
    short_code      TEXT PRIMARY KEY,
    run_id          TEXT REFERENCES runs (run_id) ON DELETE CASCADE,
    campaign_id     TEXT NOT NULL,
    destination_url TEXT NOT NULL,
    tracked_url     TEXT,
    clicks          INTEGER NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS campaign_metrics (
    run_id          TEXT NOT NULL REFERENCES runs (run_id) ON DELETE CASCADE,
    campaign_id     TEXT NOT NULL,
    channel         TEXT,
    impressions     INTEGER NOT NULL DEFAULT 0,
    clicks          INTEGER NOT NULL DEFAULT 0,
    visits          INTEGER NOT NULL DEFAULT 0,
    wishlists       INTEGER NOT NULL DEFAULT 0,
    downloads       INTEGER NOT NULL DEFAULT 0,
    spend           NUMERIC(12, 2) NOT NULL DEFAULT 0,
    email_opens     INTEGER NOT NULL DEFAULT 0,
    email_clicks    INTEGER NOT NULL DEFAULT 0,
    reddit_views    INTEGER NOT NULL DEFAULT 0,
    reddit_clicks   INTEGER NOT NULL DEFAULT 0,
    discord_clicks  INTEGER NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (run_id, campaign_id)
);

CREATE TABLE IF NOT EXISTS approval_logs (
    id              BIGSERIAL PRIMARY KEY,
    run_id          TEXT,
    campaign_id     TEXT NOT NULL,
    status          TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS publishing_logs (
    id              BIGSERIAL PRIMARY KEY,
    campaign_id     TEXT NOT NULL,
    channel         TEXT,
    status          TEXT NOT NULL,
    message         TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
