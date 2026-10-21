# Docker, PostgreSQL and n8n: step by step

This guide explains how the scheduled automation works and how to set it up yourself from scratch, so you understand each piece.

---

## 1. The big picture

```
 n8n (Docker)                Pipeline API (your PC)          Pipeline (your PC)
┌──────────────────┐  HTTP  ┌──────────────────────┐ starts ┌──────────────────────────┐
│ Every 2 weeks    │ ─────▶ │ POST /runs            │ ─────▶ │ run_pipeline.py (dry-run)│
│  or "Run now"    │        │ checks X-API-Key      │        │ scrape → Ollama → Gemini │
└──────────────────┘        └──────────────────────┘        └────────────┬─────────────┘
                                                                         │ copies the run into
                                                                         ▼
                                                              PostgreSQL (Docker)
```

- **Docker** runs two programs in isolated containers, so you don't install them on Windows:
  - **PostgreSQL**: a database. The pipeline copies each run (issues, campaigns, approvals, publish logs) into it. The JSON files in `outputs/` remain the main copy.
  - **n8n**: an automation tool with a web UI. It starts things on a schedule.
- **The Pipeline API** (`services/pipeline_api.py`) is a small web server on your PC. n8n can't run Python on your PC directly, so it calls this API, and the API starts `run_pipeline.py`.

### Is it automated?

| Step | Automated? |
|---|---|
| Scrape → analyse → generate ads → dry-run preview, every 2 weeks (Monday 06:00) | **Yes**, once the workflow is active and the pieces below are running |
| Copying results into PostgreSQL | **Yes**, every run |
| Approving campaigns | **No**, on purpose. You approve in the dashboard. |
| Actually posting to Discord / Reddit / email | **No**, on purpose. The API can only do dry-runs. You publish from the dashboard (Live mode) or with `run_pipeline.py --live`. |

For the scheduled Monday 06:00 run to happen, all of these must be up:
1. Your PC is on and **awake**. Sleep pauses everything, including Docker, n8n and a run in progress. The first test run (2026-10-21) started at 04:41, the PC slept at 04:49, and the run only finished at 11:58 after the PC woke. See section 7b.
2. Docker Desktop is running. The containers restart automatically (`restart: unless-stopped`).
3. Ollama is running.
4. **The Pipeline API is running.** This is the one piece that doesn't start by itself; see step 7 to make it start at login.

---

## 2. The credentials, and why nobody gives them to you

Gemini, Reddit and SMTP credentials come **from a provider**. The Postgres and n8n ones don't: **you invent them**, because they protect services that run on your own machine. Any long random string works.

| Variable | What it is | Value |
|---|---|---|
| `POSTGRES_USER` | database username | any name, e.g. `steam` |
| `POSTGRES_PASSWORD` | database password | long random string |
| `POSTGRES_DB` | database name | e.g. `steam_ads` |
| `POSTGRES_PORT` | port on your PC | `5432` (change only if it's taken) |
| `DATABASE_URL` | how Python finds the DB | `postgresql://USER:PASSWORD@localhost:PORT/DB`, using the **same** user/password/db as above |
| `N8N_ENCRYPTION_KEY` | n8n encrypts saved credentials with this | long random string. **Never change it later**, or n8n can't read what it saved. |
| `GENERIC_TIMEZONE` | timezone for "06:00" | e.g. `Asia/Kolkata` |
| `PIPELINE_API_TOKEN` | password n8n sends to the API (`X-API-Key` header) | long random string |
| `PIPELINE_API_URL` | where n8n finds the API | `http://host.docker.internal:8001` (`host.docker.internal` = "your PC", seen from inside Docker) |

### Generate random values

In PowerShell:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Run it once per secret and paste each result into `.env`. Hex strings (0-9, a-f) are safe inside `DATABASE_URL` because they contain no `@`, `:` or `/`.

> Never commit `.env`; it is in `.gitignore`.

---

## 3. Start PostgreSQL and n8n

From the repo root:

```powershell
docker compose up -d        # start both in the background
docker compose ps           # both should show "running"
docker compose logs -f n8n  # watch the logs (Ctrl+C to stop watching)
```

How it works: `docker-compose.yml` describes both containers. `${POSTGRES_PASSWORD}` and similar are filled in from `.env`. Data lives in Docker **volumes** (`postgres_data`, `n8n_data`), so it survives restarts.

**First start only:** Postgres runs `Pipeline/Analyze/database/schema.sql` and creates the 8 tables. If you change `POSTGRES_PASSWORD` later, the existing database **keeps the old password**. To start over, run `docker compose down -v`, which deletes all DB and n8n data.

Check the tables:

```powershell
docker compose exec postgres psql -U steam -d steam_ads -c "\dt"
```

---

## 4. Open n8n and create your account

1. Go to http://localhost:5678
2. The first visit asks you to create an **owner account** (email + password). This account is local to your n8n and isn't sent anywhere. Pick any email and a password you'll remember.
3. You'll see the workflow **"Steam pipeline - dry-run every 2 weeks"**.

---

## 5. Start the Pipeline API

In a new terminal (leave it open):

```powershell
cd Pipeline\Analyze
python -m uvicorn services.pipeline_api:app --host 127.0.0.1 --port 8001
```

Test it from another terminal:

```powershell
Invoke-RestMethod http://127.0.0.1:8001/health      # → status: ok
```

The API reads `PIPELINE_API_TOKEN` from `.env` itself. Without that header it answers `401`, and if it asks for more than 500 reviews it answers `422`.

---

## 6. The workflow

It has three nodes:

- **Every 2 weeks (Mon 06:00)** (Schedule Trigger) starts it automatically. To change it, open the node and set *Weeks Between Triggers*, the weekday and the hour.
- **Run now** (Manual Trigger) runs it when you click *Execute workflow* in the editor.
- **Start dry-run** (HTTP Request) sends `POST {PIPELINE_API_URL}/runs` with header `X-API-Key: {PIPELINE_API_TOKEN}` and body `{"app_id": 3297310, "max_reviews": 200}`.

To change the game: open **Start dry-run**, edit `app_id`, save, and publish.

Import / activate it from the command line (this was already done for you):

```powershell
docker compose exec -u node n8n n8n import:workflow --input=/workflows/scheduled_dry_run.json
docker compose exec -u node n8n n8n publish:workflow --id=steamDryRunDaily
docker compose restart n8n
docker compose exec -u node n8n n8n list:workflow --active=true
```

In n8n 2.x an "active" workflow is a **published** one. Changes made from the CLI need an n8n restart.

### Check a run

- n8n UI → **Executions** shows each trigger and whether the HTTP call succeeded.
- `POST /runs` returns a `job_id`. Then:

  ```powershell
  $h = @{ "X-API-Key" = "<your PIPELINE_API_TOKEN>" }
  Invoke-RestMethod http://127.0.0.1:8001/runs/<job_id> -Headers $h
  ```

- Full log: `Pipeline/Analyze/outputs/api_runs/<job_id>.log`
- Results: the newest `Pipeline/Analyze/outputs/run_<timestamp>/` folder, plus Postgres:

  ```powershell
  docker compose exec postgres psql -U steam -d steam_ads -c "select run_id, game_name, review_count from runs order by run_id desc limit 5"
  ```

---

## 7. Make the API start by itself (optional)

Without this, the scheduled run fails whenever you haven't started the API. Windows Task Scheduler can start it when you log in:

1. Open **Task Scheduler** → **Create Task…**
2. **General**: name `Steam Pipeline API`, select *Run only when user is logged on*.
3. **Triggers** → New → *At log on*.
4. **Actions** → New → *Start a program*:
   - Program: the full path of `python.exe` (find it with `(Get-Command python).Source`)
   - Arguments: `-m uvicorn services.pipeline_api:app --host 127.0.0.1 --port 8001`
   - Start in: the full path of your repo's `Pipeline\Analyze` folder (e.g. `C:\Projects\SteamAdReview\Pipeline\Analyze`)
5. **Conditions**: untick *Start the task only if the computer is on AC power* if you use a laptop.
6. Also enable **Docker Desktop → Settings → General → Start Docker Desktop when you sign in**.

---

## 7b. Keep the PC awake for the scheduled run

Pick one:

- **Never sleep while plugged in** (simplest): Settings → System → Power & battery → Screen, sleep & hibernate timeouts → *When plugged in, put my device to sleep after* → **Never**. Or in PowerShell:

  ```powershell
  powercfg /change standby-timeout-ac 0
  ```

- **Wake up for it**: in Task Scheduler create a task that triggers every 2 weeks on Monday at **05:55**, tick *Conditions → Wake the computer to run this task*, with action Program `cmd.exe`, Arguments `/c exit`. Also allow wake timers: Control Panel → Power Options → Change plan settings → Advanced → Sleep → *Allow wake timers* → **Enable**. The PC can go back to sleep after the idle timeout, so combine this with a longer sleep timeout (a run takes ~5-10 minutes).
- **Move the schedule** to a time you're usually at the PC: open *Every 2 weeks (Mon 06:00)* in n8n, change the day or hour, then save and publish.

To see when the PC slept and woke:

```powershell
Get-WinEvent -FilterHashtable @{LogName='System'; Id=42,107} -MaxEvents 10 | Select-Object TimeCreated, Message
```

---

## 8. Everyday commands

| Want to | Command (repo root) |
|---|---|
| Start | `docker compose up -d` |
| Stop (keeps data) | `docker compose stop` |
| Status | `docker compose ps` |
| Logs | `docker compose logs -f n8n` |
| Delete everything, start fresh | `docker compose down -v` (**erases DB + n8n data**) |

## 9. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `Set POSTGRES_PASSWORD in .env` | `.env` is missing that line; see section 2 |
| n8n execution: `ECONNREFUSED host.docker.internal:8001` | The Pipeline API isn't running (section 5) |
| n8n execution: `401` | `PIPELINE_API_TOKEN` in `.env` changed after n8n started. Run `docker compose up -d` again to reload it. |
| `409` from `/runs` | A run is already in progress; only one at a time |
| `[DB] Postgres unavailable` in pipeline output | Docker/Postgres isn't running. The pipeline still finishes and only the copy into Postgres is skipped. |
| `password authentication failed` | `DATABASE_URL` password ≠ the password the DB was first created with (section 3) |
