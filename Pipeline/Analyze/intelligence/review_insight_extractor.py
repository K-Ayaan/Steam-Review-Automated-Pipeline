import hashlib
import json
import os
from collections import Counter

import requests


SENTIMENTS = [

    "positive",

    "negative",

    "mixed",

    "neutral"
]

EMOTIONS = [

    "joy",

    "excitement",

    "fear",

    "tension",

    "satisfaction",

    "amusement",

    "nostalgia",

    "frustration",

    "anger",

    "boredom",

    "disappointment",

    "confusion"
]

DEFAULT_SEGMENTS = [

    "Horror Fans",

    "Friend Groups",

    "Co-op Players",

    "Competitive Players",

    "Casual Players",

    "Story Driven Players",

    "Builders",

    "Long-Term Players",

    "Streamers & Viewers"
]


class ReviewInsightExtractor:

    def __init__(

        self,

        segments=None
    ):

        self.url = "http://localhost:11434/api/generate"

        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

        self.segments = (

            list(segments)

            if segments

            else DEFAULT_SEGMENTS
        )

        self.cache_file = "data/insight_cache.json"

        if os.path.exists(

            self.cache_file
        ):

            with open(

                self.cache_file,

                "r",

                encoding="utf-8"

            ) as f:

                self.cache = json.load(f)

        else:

            self.cache = {}

    def build_prompt(

        self,

        review
    ):

        return f"""
Analyze this Steam game review.

Return ONLY valid JSON:

{{
  "sentiment": one of {SENTIMENTS},
  "emotions": up to 3 of {EMOTIONS},
  "topics": up to 3 short lowercase topics the player talks about (1-3 words each),
  "player_segment": exactly one of {self.segments + ["Other"]}
}}

Rules:

- Use only the allowed values for sentiment, emotions and player_segment.
- player_segment is the kind of player who wrote the review.
- Do NOT explain.

REVIEW:
{review[:1500]}
"""

    def validate(

        self,

        parsed
    ):

        sentiment = str(
            parsed.get("sentiment", "")
        ).lower()

        if sentiment not in SENTIMENTS:

            sentiment = "neutral"

        emotions = [

            str(e).lower()

            for e in parsed.get("emotions", [])

            if str(e).lower() in EMOTIONS
        ][:3]

        topics = [

            str(t).lower().strip()

            for t in parsed.get("topics", [])

            if str(t).strip()
        ][:3]

        segment = parsed.get(
            "player_segment",
            "Other"
        )

        if segment not in self.segments:

            segment = "Other"

        return {

            "sentiment":
            sentiment,

            "emotions":
            emotions,

            "topics":
            topics,

            "player_segment":
            segment
        }

    def extract(

        self,

        review
    ):

        review = str(review)

        key = hashlib.md5(

            (",".join(self.segments) + review).encode(
                "utf-8"
            )

        ).hexdigest()

        if key in self.cache:

            return self.cache[key]

        response = requests.post(

            self.url,

            json={

                "model": self.model,

                "prompt": self.build_prompt(review),

                "stream": False,

                "format": "json",

                "options": {

                    "temperature": 0,

                    "num_predict": 150
                }
            },

            timeout=300
        )

        response.raise_for_status()

        raw = response.json().get(
            "response",
            ""
        )

        try:

            parsed = json.loads(raw)

        except json.JSONDecodeError:

            parsed = {}

        result = self.validate(parsed)

        self.cache[key] = result

        return result

    def save_cache(self):

        with open(

            self.cache_file,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                self.cache,

                f,

                ensure_ascii=False,

                indent=2
            )

    def extract_all(

        self,

        df
    ):

        rows = []

        for i, row in enumerate(

            df.itertuples(),

            start=1
        ):

            print(
                f"Insights {i}/{len(df)}"
            )

            rows.append({

                "review_id":
                row.review_id,

                **self.extract(
                    row.review_text
                )
            })

            if i % 10 == 0:

                self.save_cache()

        self.save_cache()

        return rows

    def summarize(

        self,

        rows
    ):

        def block(items):

            emotions = Counter(

                e

                for r in items

                for e in r["emotions"]
            )

            topics = Counter(

                t

                for r in items

                for t in r["topics"]
            )

            return {

                "count":
                len(items),

                "sentiment":
                dict(Counter(r["sentiment"] for r in items)),

                "top_emotions":
                [e for e, _ in emotions.most_common(5)],

                "top_topics":
                [t for t, _ in topics.most_common(5)],

                "emotion_counts":
                dict(emotions.most_common(10)),

                "topic_counts":
                dict(topics.most_common(15))
            }

        segments = {}

        for segment in sorted(

            {r["player_segment"] for r in rows}
        ):

            segments[segment] = block([

                r

                for r in rows

                if r["player_segment"] == segment
            ])

        return {

            **block(rows),

            "segments":
            segments
        }
