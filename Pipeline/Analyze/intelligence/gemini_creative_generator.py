import json
import os
import threading

from google import genai


DEFAULT_GEMINI_MODEL = "gemini-3.8-flash"

# Gemini can take a long time under load (up to ~30 min), but a
# connection Google drops mid-request would otherwise hang the
# pipeline forever. interactions.create ignores the client's
# http_options timeout, so it is passed per request.

REQUEST_TIMEOUT_SECONDS = int(

    os.getenv(

        "GEMINI_TIMEOUT_SECONDS",

        "1800"
    )
)

# The SDK can still block past its own timeout (half-closed socket,
# long server-requested retry delays), so each attempt also gets a
# hard wall-clock deadline.

HARD_TIMEOUT_SECONDS = REQUEST_TIMEOUT_SECONDS + 60

ATTEMPTS = 3


def call_with_deadline(

    fn,

    seconds
):

    result = {}

    def run():

        try:

            result["value"] = fn()

        except BaseException as e:

            result["error"] = e

    # Daemon thread: an attempt stuck inside the SDK
    # cannot keep the process alive.

    worker = threading.Thread(

        target=run,

        daemon=True
    )

    worker.start()

    worker.join(seconds)

    if worker.is_alive():

        raise TimeoutError(
            f"no response from Gemini after {seconds}s"
        )

    if "error" in result:

        raise result["error"]

    return result["value"]

CREATIVE_SCHEMA = {

    "type": "object",

    "properties": {

        "headline": {"type": "string"},

        "discord_post": {"type": "string"},

        "reddit_title": {"type": "string"},

        "reddit_post": {"type": "string"},

        "email_subject": {"type": "string"},

        "email_body": {"type": "string"},

        "cta": {"type": "string"}
    },

    "required": [

        "headline",

        "discord_post",

        "reddit_title",

        "reddit_post",

        "email_subject",

        "email_body",

        "cta"
    ]
}


def channel_creatives(

    creatives,

    platform
):

    # Map the shared Gemini package onto the
    # headline / ad_copy / cta keys publishers read.

    channel = dict(creatives)

    if platform == "reddit":

        channel["headline"] = creatives.get(
            "reddit_title",
            creatives.get("headline", "")
        )

        channel["ad_copy"] = creatives.get(
            "reddit_post",
            ""
        )

    elif platform == "email":

        channel["headline"] = creatives.get(
            "email_subject",
            creatives.get("headline", "")
        )

        channel["ad_copy"] = creatives.get(
            "email_body",
            ""
        )

    else:

        channel["ad_copy"] = creatives.get(
            "discord_post",
            ""
        )

    return channel


class GeminiCreativeGenerator:

    def __init__(

        self,

        api_key=None,

        model=None
    ):

        api_key = (

            api_key

            or

            os.getenv(
                "GEMINI_API_KEY"
            )
        )

        if not api_key:

            raise ValueError(
                "GEMINI_API_KEY is not set"
            )

        self.api_key = api_key

        self.client = genai.Client(

            api_key=api_key
        )

        self.model = (

            model

            or

            os.getenv(

                "GEMINI_MODEL",

                DEFAULT_GEMINI_MODEL
            )
        )

    def build_prompt(

        self,

        context
    ):

        insights = context.get(
            "insights",
            {}
        )

        return f"""
You are a senior AAA game marketing copywriter.

Game:
{context['game_name']}

Genre:
{context['genre']}

Core Pillars:
{context.get('pillars', [])}

Audience:
{context['audience']}

Promote:
{context['promote']}

Avoid:
{context['avoid']}

What this audience feels (from player reviews):
{insights.get('top_emotions', [])}

What this audience talks about (from player reviews):
{insights.get('top_topics', [])}

Audience sentiment:
{insights.get('sentiment', {})}

Write one campaign for this audience with a separate variant per channel.

Channel Rules:

Discord
- Short announcement
- Exciting
- Community focused
- Under 80 words

Reddit
- Conversational
- Community driven
- Discussion focused
- Title under 120 characters
- Post under 120 words

Email
- Professional
- Personalized to the audience
- CTA driven
- Subject under 60 characters
- Body under 150 words

Rules:

1. Match the genre and the audience.
2. Use only the provided pillars and strengths.
3. Never invent game features. Do not name specific enemies, ghosts,
   monsters, characters, locations, weapons or mechanics unless they
   appear in the pillars or promote list above.
4. Never invent a game name.
5. Never mention avoided topics.
6. Keep the CTA under 10 words.
7. Do not include URLs; a tracking link is appended later.
"""

    def generate(

        self,

        context
    ):

        # Retry timeouts, dropped connections and malformed output.

        for attempt in range(1, ATTEMPTS + 1):

            try:

                return call_with_deadline(

                    lambda: self.generate_once(
                        context
                    ),

                    HARD_TIMEOUT_SECONDS
                )

            except Exception as e:

                if attempt == ATTEMPTS:

                    raise

                print(
                    f"[Gemini] attempt {attempt} failed "
                    f"({type(e).__name__}), retrying"
                )

                if isinstance(e, TimeoutError):

                    # The stuck attempt may hold a dead pooled
                    # connection: retry on a fresh client.

                    self.client = genai.Client(

                        api_key=self.api_key
                    )

    def generate_once(

        self,

        context
    ):

        interaction = self.client.interactions.create(

            model=self.model,

            input=self.build_prompt(
                context
            ),

            response_format={

                "type": "text",

                "mime_type": "application/json",

                "schema": CREATIVE_SCHEMA
            },

            timeout=REQUEST_TIMEOUT_SECONDS
        )

        text = (

            interaction.output_text

            or

            ""
        ).strip()

        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        ).strip()

        try:

            creatives = json.loads(text)

        except json.JSONDecodeError:

            raise ValueError(

                f"Gemini returned non-JSON output: {text[:200]}"
            )

        missing = [

            key

            for key in CREATIVE_SCHEMA["required"]

            if not creatives.get(key)
        ]

        if missing:

            raise ValueError(

                f"Gemini output missing fields: {missing}"
            )

        return creatives
