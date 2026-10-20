class IssueValidator:

    ALLOWED_IDS = {

        "NO_ISSUE",

        "ANTI_CHEAT_CHEATERS",
        "ANTI_CHEAT_VAC_VERIFICATION",

        "MATCHMAKING",

        "PERFORMANCE_FPS",

        "SERVER_LATENCY",

        "CONTENT_DROUGHT",

        "GAMEPLAY_BALANCE",

        "UI_UX",

        "CRASHES",

        "BUGS",

        "COMMUNITY_TOXICITY",

        "REGIONAL_MATCHMAKING",

        "SKIN_ECONOMY",

        "MULTIPLAYER_CONNECTIVITY",

        "MULTIPLAYER_FUN",

        "HORROR_EXPERIENCE",

        "HORROR_EFFECTIVENESS",

        "IMMERSION",

        "AUDIO_IMMERSION",

        "CONTENT_REQUESTS",

        "REPLAYABILITY",

        "GAMEPLAY_CLARITY",

        "TUTORIAL_ONBOARDING",

        "UI_UX_PROBLEMS",

        "LOCALIZATION",

        "SERVER_CONNECTIVITY"
    }

    VALID_SENTIMENTS = {
        "positive",
        "negative",
        "neutral"
    }

    def validate(self, llm_result):

        if "issues" not in llm_result:

            return {
                "issues": [
                    {
                        "issue_id": "NO_ISSUE",
                        "sentiment": "neutral",
                        "evidence": ""
                    }
                ]
            }

        cleaned_issues = []

        for issue in llm_result["issues"]:

            issue_id = issue.get(
                "issue_id",
                "NO_ISSUE"
            )

            sentiment = issue.get(
                "sentiment",
                "neutral"
            )

            if issue_id not in self.ALLOWED_IDS:

                issue_id = "NO_ISSUE"

            if sentiment not in self.VALID_SENTIMENTS:

                sentiment = "neutral"

            if issue_id != "NO_ISSUE":

                cleaned_issues.append({

                    "issue_id": issue_id,

                    "sentiment": sentiment,

                    "evidence": issue.get(

                        "evidence",

                        ""
                    )

                })

        if len(cleaned_issues) == 0:

            cleaned_issues.append({

                "issue_id": "NO_ISSUE",

                "sentiment": "neutral",

                "evidence": ""

            })

        return {

            "issues": cleaned_issues

        }