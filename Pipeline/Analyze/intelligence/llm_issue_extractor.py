import requests
import hashlib
import os
import json
from intelligence.issue_validator import (
    IssueValidator
)


class LLMIssueExtractor:

    def __init__(self):

        self.url = "http://localhost:11434/api/generate"

        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
        # self.model = "gemma3:12b"

        self.validator = IssueValidator()

        self.cache_file = "data/llm_cache.json"

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

    def extract(self, review):

        review_lower = review.lower()

        if (

            "my friend" in review_lower

            or

            "college days" in review_lower

            or

            "great memories" in review_lower

        ):

            return {

                "issues": [

                    {

                        "issue_id": "NO_ISSUE",

                        "sentiment": "neutral"

                    }

                ]
            }

        review_hash = hashlib.md5(

            review.encode(

                "utf-8"

            )

        ).hexdigest()

        if review_hash in self.cache:

            return self.cache[
                review_hash
            ]

        prompt = f"""
Classify the game review.

CRITICAL RULES:

- Return ONLY valid JSON.
- Use ONLY allowed issue IDs.
- Maximum 5 issues.
- Do NOT explain.
- Do NOT invent categories.
- Do NOT guess.

IMPORTANT:

If unsure, return NO_ISSUE.

False positives are worse than missed issues.

NO_ISSUE MUST be returned for:

- account theft stories
- trade scams
- marketplace scams
- inventory scams
- API hijacking stories
- Steam trading stories
- skin jokes
- knife jokes
- inventory jokes
- gambling jokes
- loot box jokes
- cosmetic item jokes
- nostalgia stories
- personal gaming history
- scam warnings unrelated to gameplay
- trading stories
- marketplace stories
- player memories
- story summaries
- lore descriptions
- plot descriptions
- store page text
- game descriptions
- feature descriptions
- marketing text
- praise only
- jokes
- memes
- emotional reactions
- reviews without actionable feedback

Allowed issue IDs:

BUGS
CRASHES
PERFORMANCE_FPS
SERVER_CONNECTIVITY
SERVER_LATENCY
MULTIPLAYER_CONNECTIVITY
MULTIPLAYER_FUN
HORROR_EXPERIENCE
HORROR_EFFECTIVENESS
IMMERSION
AUDIO_IMMERSION
CONTENT_REQUESTS
REPLAYABILITY
GAMEPLAY_CLARITY
TUTORIAL_ONBOARDING
UI_UX_PROBLEMS
LOCALIZATION
GAMEPLAY_BALANCE
COMMUNITY_TOXICITY
NO_ISSUE

ADDITIONAL RULES:

Every issue MUST contain:

- issue_id
- sentiment
- evidence

Evidence rules:

- Copy exact words from the review.
- Do NOT summarize.
- Do NOT invent text.
- Maximum 20 words.
- Evidence must directly support the issue.

Example:

Review:
The game crashes every time I join a lobby.

Output:

{{
  "issues":[
    {{
      "issue_id":"CRASHES",
      "sentiment":"negative",
      "evidence":"crashes every time I join a lobby"
    }}
  ]
}}

Example:

Review:
Players instantly die after spawning.

Output:

{{
  "issues":[
    {{
      "issue_id":"BUGS",
      "sentiment":"negative",
      "evidence":"instantly die after spawning"
    }}
  ]
}}

Example:

Review:
The game is boring and repetitive.

Output:

{{
  "issues":[
    {{
      "issue_id":"GAMEPLAY_CLARITY",
      "sentiment":"negative",
      "evidence":"boring and repetitive"
    }}
  ]
}}

Format:

{{
  "issues":[
    {{
      "issue_id":"BUGS",
      "sentiment":"negative",
      "evidence":"players die instantly at game start"
    }}
  ]
}}

REVIEW:
"""
        prompt += review

        response = requests.post(

          self.url,

          json={

            "model": self.model,

            "prompt": prompt,

            "stream": False,

            "options": {

                "temperature": 0,

                "num_predict": 150

            }
          }
        )

        result = response.json()

        raw_output = result.get(
            "response",
            ""
        )

        raw_output = (
            raw_output
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:

            parsed = json.loads(
            raw_output
        )

        except:

            parsed = {
                "issues": [
                    {
                        "issue_id": "NO_ISSUE",
                        "sentiment": "neutral"
                    }
                ]
            }

        validated = (
            self.validator.validate(
                parsed
            )
        )

        issues = validated.get(
            "issues",
            []
        )

        real_issues = [

            issue

            for issue in issues

            if issue["issue_id"]
            != "NO_ISSUE"
        ]

        if real_issues:

            validated["issues"] = (
                real_issues
            )

        self.cache[
            review_hash
        ] = validated

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

        return validated