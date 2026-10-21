# Steam Game Intelligence & Marketing Automation

Enter a Steam App ID. The pipeline then:

1. scrapes the game's Steam reviews,
2. preprocesses them (playtime, engagement, language),
3. runs a local **Ollama** model over each review for sentiment, emotions, topics and player segment, plus rule/LLM issue extraction, health scores and audience profiling,
4. asks **Gemini** for genre-specific, audience-specific ads with separate **Discord / Reddit / Email** variants,
5. distributes them to Discord, Reddit and email. **Dry-run by default; nothing is sent unless you pass `--live`.**
6. A **Streamlit** dashboard shows sentiment, sales estimates and competitors, and can run the pipeline and trigger distribution.
7. Optionally, **n8n** (Docker) runs it on a schedule, and **PostgreSQL** (Docker) keeps a copy of every run.

## Project structure

```
docker-compose.yml          PostgreSQL + n8n
docs/                       setup guides (Docker / n8n step by step)
n8n/workflows/              importable n8n workflow (scheduled dry-run)
Pipeline/
  requirements.txt
  Scraper-main/             Steam review scraper
  Analyze/
    run_pipeline.py         one command: App ID → reviews → insights → ads → distribution
    generate_dataset.py     preprocessing (playtime, engagement, language)
    pipeline/               full analysis (issues, health, audiences, campaigns, reports)
    intelligence/           Ollama insights, segmentation, Gemini ad generation, scoring
    reports/                executive / developer / segment / trend reports, PDF export
    services/               Steam market data, publisher, logging, pipeline API for n8n
    publishers/             Reddit (PRAW) and email (SMTP) senders
    database/               PostgreSQL schema + mirror
    dashboard/              Streamlit app
    config/                 analysis config, game profiles, genre rule sets
    test/                   pytest smoke tests
```

## Requirements

- Python 3.14 (the version this was built and tested on)
- [Ollama](https://ollama.com) running locally, with a model pulled, e.g. `ollama pull qwen2.5:7b-instruct`
- A Gemini API key (https://aistudio.google.com/apikey) for ad generation. Without one, the pipeline falls back to Ollama ads and marks them `generated_by: "ollama"`.

## Setup

```bash
cd Pipeline
python -m pip install -r requirements.txt
```

Fill in the values in the repo-root `.env`. It ships with blank placeholders; see `.env.example` for the expected format of each value.
`.env` is loaded automatically. Blank values are ignored, and variables already set in your shell take precedence.

### Environment variables

| Variable | Needed for | Notes |
|---|---|---|
| `GEMINI_API_KEY` | ad generation | |
| `GEMINI_MODEL` | ad generation | default `gemini-3.8-flash` |
| `OLLAMA_MODEL` | review analysis | default `qwen2.5:7b`; set it to the tag shown by `ollama list` (e.g. `qwen2.5:7b-instruct`) |
| `DISCORD_WEBHOOK_URL` | live Discord | falls back to `config/discord_config.py` |
| `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD`, `REDDIT_SUBREDDIT` | live Reddit | create a "script" app at https://www.reddit.com/prefs/apps |
| `REDDIT_USER_AGENT` | live Reddit | optional |
| `SMTP_HOST`, `SMTP_FROM`, `EMAIL_RECIPIENTS` | live email | `EMAIL_RECIPIENTS` is comma-separated |
| `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_USE_TLS` | live email | defaults: `587`, none, none, `true`. Port `465` uses implicit SSL; other ports use STARTTLS when `SMTP_USE_TLS=true` |

Dry-run mode needs none of the Discord/Reddit/SMTP variables.

## Run the whole pipeline (one command)

All commands run from `Pipeline/Analyze`:

```bash
cd Pipeline/Analyze
python run_pipeline.py --app-id 3297310
```

This scrapes up to 20 review pages (capped at `--max-reviews`, default 200), then preprocesses, analyses, generates ads, and prints a **dry-run** of every Discord/Reddit/Email message.
The results go to `outputs/run_<timestamp>/`. The main files are `segment_campaigns.json` (ads per audience × channel), `insights.json` (Ollama sentiment/emotions/topics/segments) and `market_report.json` (sales + competitors).

Useful flags:

| Flag | Meaning |
|---|---|
| `--max-reviews N` / `--max-pages N` | limit scraping (default 200 / 20) |
| `--skip-scrape` | reuse the existing `data/reviews.csv` |
| `--start-date` / `--end-date` | review date window (default 2000-01-01 to today) |
| `--competitors 730 892970 ...` | competitor App IDs (default: a built-in list) |
| `--channels discord reddit email` | restrict distribution channels |
| `--skip-distribute` | stop after ad generation |
| `--live` | **really send**, and only campaigns whose status is `APPROVED` (approve them in the dashboard first) |

Note that each run overwrites `data/reviews.csv`, `data/preprocessed_reviews.csv`, `data/language_reviews.csv`, `data/unknown_reviews.csv` and `data/review_insights.csv`.

## Dashboard

```bash
cd Pipeline/Analyze
python -m streamlit run dashboard/app.py
```

- **💬 Sentiment / 💰 Sales / 🥊 Competitors** show the selected run's `insights.json` / `market_report.json`, falling back to cached data in `data/` for older runs.
- **⚙ Analysis Runner → Run Full Pipeline** runs `run_pipeline.py` for an App ID (dry-run distribution).
- **📤 Campaign Approval** is where you approve or reject the generated ads.
- **🚀 Publishing Queue** has a *Live mode* toggle, off by default. With it off, *Publish* / *Distribute all approved* only preview the messages.

Click counting is not active. Posts link to the Steam store URL with UTM tags, and a public URL shortener is planned as a separate project.

## PostgreSQL + n8n (Docker, optional)

Everything above works without Docker. With it, each run is also mirrored into PostgreSQL, and n8n can start dry-runs on a schedule.

New to Docker or n8n? Follow the step-by-step guide: [docs/DOCKER_N8N_GUIDE.md](docs/DOCKER_N8N_GUIDE.md).

1. Add the PostgreSQL / n8n block from `.env.example` to `.env`. Use real random values for `POSTGRES_PASSWORD`, `N8N_ENCRYPTION_KEY` and `PIPELINE_API_TOKEN`, and put the same password in `DATABASE_URL`.
2. From the repo root:

   ```bash
   docker compose up -d
   ```

   Postgres listens on `localhost:5432`, n8n on http://localhost:5678. The tables in `Pipeline/Analyze/database/schema.sql` (games, runs, issues, campaigns, campaign_links, campaign_metrics, approval_logs, publishing_logs) are created on the first start only. To recreate them, run `docker compose down -v`, which **deletes the data**.
3. Once `DATABASE_URL` is set, `run_pipeline.py` mirrors each run, the dashboard mirrors approvals and rejections, and every publish is mirrored from the publishing log. If Postgres is down, a one-line `[DB]` warning is printed and the pipeline carries on.

### Scheduled runs with n8n

n8n calls a small API that starts `run_pipeline.py`. **Always dry-run**, capped at 500 reviews, one run at a time, and it needs the `X-API-Key: $PIPELINE_API_TOKEN` header.

```bash
cd Pipeline/Analyze
python -m uvicorn services.pipeline_api:app --host 127.0.0.1 --port 8001
```

- `POST /runs` with `{"app_id": 3297310, "max_reviews": 200}` returns a `job_id`, and `GET /runs/{job_id}` returns its status and the last log lines. Logs go to `outputs/api_runs/`.
- Import the sample workflow (daily at 06:00, inactive until you switch it on):

  ```bash
  docker compose exec -u node n8n n8n import:workflow --input=/workflows/scheduled_dry_run.json
  ```

  Change the `app_id` in its *Start dry-run* node, then activate it in the n8n UI.

Live sending stays manual: approve campaigns in the dashboard and publish there, or run `run_pipeline.py --live`.

## Tests

```bash
cd Pipeline/Analyze
python -m pytest test
```

The Postgres round-trip test is skipped unless `TEST_DATABASE_URL` points at a disposable database. It writes rows and then removes them.

## Sales data caveat

Steam publishes no sales figures. "Sales" combines Steam Store price + review totals with SteamSpy's owner-estimate range. Revenue is estimated as the midpoint of the owner range × current price. Treat it as a rough indicator, not reported revenue.
