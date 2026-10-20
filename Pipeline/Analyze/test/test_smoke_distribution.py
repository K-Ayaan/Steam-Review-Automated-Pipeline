import os
import sys

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

import pytest

from publishers import email_publisher, reddit_publisher

from services import publisher as publisher_module


CAMPAIGN = {

    "campaign_id": "the_cursed_hour_horror_fans_reddit",

    "audience": "Horror Fans",

    "channel": "Reddit",

    "platform": "reddit",

    "tracking_url": "https://store.steampowered.com/app/3297310?utm_source=reddit",

    "tracked_url": "http://localhost:8000/r/abc",

    "creatives": {

        "headline": "Headline",

        "ad_copy": "Copy",

        "reddit_title": "Reddit title",

        "reddit_post": "Reddit copy",

        "email_subject": "Email subject",

        "email_body": "Email copy",

        "cta": "Wishlist Now"
    }
}


@pytest.fixture(autouse=True)
def no_logging(monkeypatch, tmp_path):

    # Keep tests from touching outputs/publishing_logs.json
    # and from seeing real credentials loaded from .env

    for name in list(os.environ):

        if name.startswith(("REDDIT_", "SMTP_", "EMAIL_", "DISCORD_")):

            monkeypatch.delenv(name)

    logged = []

    monkeypatch.setattr(
        publisher_module.PublishingLogger,
        "log",
        lambda self, **kw: logged.append(kw)
    )

    return logged


def test_reddit_dry_run_does_not_call_api(monkeypatch, capsys):

    monkeypatch.setattr(
        reddit_publisher.praw,
        "Reddit",
        lambda **kw: pytest.fail("praw called in dry-run")
    )

    result = reddit_publisher.RedditPublisher().publish(CAMPAIGN)

    assert result["posted"] is False

    assert result["title"] == "Reddit title"

    assert "Reddit copy" in result["body"]

    assert CAMPAIGN["tracking_url"] in result["body"]

    assert "[DRY-RUN] Reddit" in capsys.readouterr().out


def test_reddit_live_requires_env(monkeypatch):

    for name in reddit_publisher.REQUIRED_ENV:

        monkeypatch.delenv(name, raising=False)

    with pytest.raises(ValueError):

        reddit_publisher.RedditPublisher().publish(CAMPAIGN, dry_run=False)


def test_reddit_live_submits(monkeypatch):

    for name in reddit_publisher.REQUIRED_ENV:

        monkeypatch.setenv(name, "x")

    submitted = {}

    class FakeSubreddit:

        def submit(self, title, selftext):

            submitted.update(title=title, selftext=selftext)

            return type("S", (), {"id": "p1", "permalink": "/r/x/p1"})()

    class FakeReddit:

        def __init__(self, **kw):
            pass

        def subreddit(self, name):
            return FakeSubreddit()

    monkeypatch.setattr(reddit_publisher.praw, "Reddit", FakeReddit)

    result = reddit_publisher.RedditPublisher().publish(CAMPAIGN, dry_run=False)

    assert result["posted"] is True

    assert result["post_id"] == "p1"

    assert submitted["title"] == "Reddit title"


def test_email_dry_run_does_not_connect(monkeypatch, capsys):

    monkeypatch.setenv("EMAIL_RECIPIENTS", "a@example.com, b@example.com")

    monkeypatch.setattr(
        email_publisher.smtplib,
        "SMTP",
        lambda *a, **kw: pytest.fail("SMTP called in dry-run")
    )

    result = email_publisher.EmailPublisher().publish(CAMPAIGN)

    assert result["sent"] is False

    assert result["subject"] == "Email subject"

    assert result["recipients"] == ["a@example.com", "b@example.com"]

    assert "[DRY-RUN] Email" in capsys.readouterr().out


def test_email_live_sends(monkeypatch):

    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")

    monkeypatch.setenv("SMTP_FROM", "me@example.com")

    monkeypatch.setenv("EMAIL_RECIPIENTS", "a@example.com")

    monkeypatch.setenv("SMTP_USERNAME", "me")

    sent = []

    class FakeSMTP:

        def __init__(self, host, port, timeout):
            sent.append(("connect", host, port))

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def starttls(self):
            sent.append("tls")

        def login(self, user, password):
            sent.append("login")

        def send_message(self, message):
            sent.append(message["Subject"])

    monkeypatch.setattr(email_publisher.smtplib, "SMTP", FakeSMTP)

    result = email_publisher.EmailPublisher().publish(CAMPAIGN, dry_run=False)

    assert result["sent"] is True

    assert sent == [("connect", "smtp.example.com", 587), "tls", "login", "Email subject"]


def test_email_port_465_uses_ssl(monkeypatch):

    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")

    monkeypatch.setenv("SMTP_PORT", "465")

    monkeypatch.setenv("SMTP_FROM", "me@example.com")

    monkeypatch.setenv("EMAIL_RECIPIENTS", "a@example.com")

    used = []

    class FakeSSL:

        def __init__(self, host, port, timeout):
            used.append(port)

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def starttls(self):
            pytest.fail("STARTTLS on implicit-SSL port")

        def send_message(self, message):
            used.append("sent")

    monkeypatch.setattr(email_publisher.smtplib, "SMTP_SSL", FakeSSL)

    monkeypatch.setattr(
        email_publisher.smtplib,
        "SMTP",
        lambda *a, **kw: pytest.fail("plain SMTP used for 465")
    )

    assert email_publisher.EmailPublisher().publish(CAMPAIGN, dry_run=False)["sent"]

    assert used == [465, "sent"]


def test_publisher_dry_run_default_never_posts(monkeypatch, no_logging):

    pub = publisher_module.Publisher()

    monkeypatch.setattr(
        pub.discord,
        "publish",
        lambda *a, **kw: pytest.fail("Discord posted in dry-run")
    )

    for platform in ["discord", "reddit", "email"]:

        assert pub.publish({**CAMPAIGN, "platform": platform})

    assert no_logging == []


def test_publisher_live_reddit_without_creds_skips(monkeypatch, no_logging):

    for name in reddit_publisher.REQUIRED_ENV:

        monkeypatch.delenv(name, raising=False)

    pub = publisher_module.Publisher()

    assert pub.publish({**CAMPAIGN, "platform": "reddit"}, dry_run=False) is False

    assert no_logging == []


def test_publisher_live_email_failure_is_logged(monkeypatch, no_logging):

    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")

    monkeypatch.setenv("SMTP_FROM", "me@example.com")

    monkeypatch.setenv("EMAIL_RECIPIENTS", "a@example.com")

    def refuse(*a, **kw):
        raise OSError("connection refused")

    monkeypatch.setattr(email_publisher.smtplib, "SMTP", refuse)

    pub = publisher_module.Publisher()

    assert pub.publish({**CAMPAIGN, "platform": "email"}, dry_run=False) is False

    assert no_logging[0]["status"] == "FAILED"


def test_publisher_live_discord_uses_env_webhook(monkeypatch, no_logging):

    monkeypatch.setenv("DISCORD_WEBHOOK_URL", "https://discord.test/hook")

    pub = publisher_module.Publisher()

    calls = []

    monkeypatch.setattr(
        pub.discord,
        "publish",
        lambda url, campaign: calls.append(url) or True
    )

    assert pub.publish({**CAMPAIGN, "platform": "discord"}, dry_run=False)

    assert calls == ["https://discord.test/hook"]

    assert no_logging[0]["status"] == "SUCCESS"
