import re
from collections import Counter
import json

rule_stats = Counter()


class RuleBasedExtractor:

    def __init__(self):

        self.rules = {}

    def load_rules(

        self,

        genre
    ):

        genre_map = {

            "Competitive FPS":

            "config/rules/fps_rules.json",

            "Co-op Horror":

            "config/rules/horror_rules.json",

            "Survival Crafting":

            "config/rules/survival_rules.json"
        }

        with open(

            "config/rules/base_rules.json",

            "r",

            encoding="utf-8"

        ) as f:

            base_rules = json.load(f)

        path = genre_map.get(
            genre
        )

        if not path:

            self.rules = base_rules

            return

        with open(

            path,

            "r",

            encoding="utf-8"

        ) as f:

            genre_rules = json.load(f)

        self.rules = {

            **base_rules,

            **genre_rules
        }

        print(
            f"koooooooooooooooooooooLoaded Genre Rules: {genre}"
        )
        print(
            f"Total Rule Categories: {len(self.rules)}"
        )

    def keyword_match(
        self,
        keyword,
        text
    ):

        keyword = keyword.lower()

        pattern = (
            rf"(?<!\w){re.escape(keyword)}(?!\w)"
        )

        return bool(
            re.search(
                pattern,
                text
            )
        )

    def extract(
        self,
        review_text
    ):

        review_text = str(
            review_text
        ).lower()

        found = []

        for issue_id, keywords in (
            self.rules.items()
        ):

            matched = False

            for keyword in keywords:

                if self.keyword_match(
                    keyword,
                    review_text
                ):

                    found.append({
                        "issue_id": issue_id,
                        "sentiment": "unknown"
                    })
                    rule_stats[issue_id] += 1

                    matched = True

                    break

            if matched:

                continue

        if not found:

            return {

                "issues": [

                    {

                        "issue_id":
                        "NO_ISSUE",

                        "sentiment":
                        "neutral"
                    }
                ]
            }

        return {

            "issues": found
        }