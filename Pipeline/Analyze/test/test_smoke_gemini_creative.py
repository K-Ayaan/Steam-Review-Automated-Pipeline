import json
import os
import sys

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

import pytest

from intelligence import gemini_creative_generator as gcg


PACKAGE = {

    "headline": "Not Every Door Should Be Opened",

    "discord_post": "Discord copy",

    "reddit_title": "Reddit title",

    "reddit_post": "Reddit copy",

    "email_subject": "Email subject",

    "email_body": "Email copy",

    "cta": "Wishlist Now"
}

CONTEXT = {

    "game_name": "The Cursed Hour",

    "genre": "Psychological Horror",

    "pillars": ["Fear", "Atmosphere"],

    "audience": "Horror Fans",

    "promote": ["Horror Atmosphere"],

    "avoid": ["Polished Experience"],

    "insights": {"top_emotions": ["fear"], "top_topics": ["atmosphere"]}
}


class FakeInteractions:

    def __init__(self, text):

        self.text = text

        self.kwargs = None

    def create(self, **kwargs):

        self.kwargs = kwargs

        return type("Interaction", (), {"output_text": self.text})()


def make_generator(monkeypatch, text):

    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    monkeypatch.delenv("GEMINI_MODEL", raising=False)

    generator = gcg.GeminiCreativeGenerator()

    generator.client = type("Client", (), {})()

    generator.client.interactions = FakeInteractions(text)

    return generator


def test_requires_api_key(monkeypatch):

    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    with pytest.raises(ValueError):

        gcg.GeminiCreativeGenerator()


def test_model_from_env(monkeypatch):

    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    monkeypatch.setenv("GEMINI_MODEL", "custom-model")

    assert gcg.GeminiCreativeGenerator().model == "custom-model"


def test_generate_returns_all_variants(monkeypatch):

    generator = make_generator(monkeypatch, "```json\n" + json.dumps(PACKAGE) + "\n```")

    result = generator.generate(CONTEXT)

    assert result == PACKAGE

    sent = generator.client.interactions.kwargs

    assert sent["model"] == gcg.DEFAULT_GEMINI_MODEL

    assert sent["response_format"]["mime_type"] == "application/json"

    assert "Horror Fans" in sent["input"]

    assert "fear" in sent["input"]


def test_generate_rejects_incomplete_output(monkeypatch):

    generator = make_generator(monkeypatch, json.dumps({"headline": "x"}))

    with pytest.raises(ValueError):

        generator.generate(CONTEXT)


def test_channel_creatives_mapping():

    assert gcg.channel_creatives(PACKAGE, "discord")["ad_copy"] == "Discord copy"

    reddit = gcg.channel_creatives(PACKAGE, "reddit")

    assert reddit["headline"] == "Reddit title"

    assert reddit["ad_copy"] == "Reddit copy"

    email = gcg.channel_creatives(PACKAGE, "email")

    assert email["headline"] == "Email subject"

    assert email["ad_copy"] == "Email copy"
