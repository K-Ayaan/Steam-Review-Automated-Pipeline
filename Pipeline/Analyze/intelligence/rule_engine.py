# class RuleEngine:

#     def extract(

#         self,

#         review

#     ):

#         review = review.lower()

#         issues = []

#         if any(

#             word in review

#             for word in [

#                 "cheater",
#                 "cheaters",
#                 "hack",
#                 "hacker"
#             ]
#         ):

#             issues.append({

#                 "issue_id":
#                 "ANTI_CHEAT_CHEATERS",

#                 "sentiment":
#                 "negative"
#             })

#         if "vac" in review:

#             issues.append({

#                 "issue_id":
#                 "ANTI_CHEAT_VAC_VERIFICATION",

#                 "sentiment":
#                 "negative"
#             })

#         if any(

#             word in review

#             for word in [

#                 "toxic",
#                 "toxicity"
#             ]
#         ):

#             issues.append({

#                 "issue_id":
#                 "COMMUNITY_TOXICITY",

#                 "sentiment":
#                 "negative"
#             })

#         if any(

#             word in review

#             for word in [

#                 "crash",
#                 "crashes",
#                 "crashed"
#             ]
#         ):

#             issues.append({

#                 "issue_id":
#                 "CRASHES",

#                 "sentiment":
#                 "negative"
#             })

#         if any(

#             word in review

#             for word in [

#                 "fps",
#                 "lag",
#                 "stutter",
#                 "stuttering"
#             ]
#         ):

#             issues.append({

#                 "issue_id":
#                 "PERFORMANCE_FPS",

#                 "sentiment":
#                 "negative"
#             })

#         return issues



import json


class RuleEngine:

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

        path = genre_map.get(
            genre
        )

        if not path:

            self.rules = {}

            return

        with open(

            path,

            "r",

            encoding="utf-8"

        ) as f:

            self.rules = json.load(f)

    def extract(

        self,

        review
    ):

        review = str(
            review
        ).lower()

        issues = []

        for issue_id, keywords in (

            self.rules.items()
        ):

            for keyword in keywords:

                if keyword.lower() in review:

                    issues.append({

                        "issue_id":
                        issue_id,

                        "sentiment":
                        "negative"
                    })

                    break

        return issues