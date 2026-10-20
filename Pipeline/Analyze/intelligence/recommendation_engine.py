class RecommendationEngine:

    RECOMMENDATIONS = {

        "ANTI_CHEAT_CHEATERS": {

            "problem":
            "Cheaters reduce competitive trust.",

            "recommendation":
            [
                "Improve anti-cheat detection",
                "Increase ban frequency",
                "Review cheat reports"
            ],

            "expected_impact":
            "Improve player retention."
        },

        "ANTI_CHEAT_VAC_VERIFICATION": {

            "problem":
            "Players cannot reliably join matches.",

            "recommendation":
            [
                "Investigate VAC validation failures",
                "Improve session verification"
            ],

            "expected_impact":
            "Reduce player frustration."
        },

        "PERFORMANCE_FPS": {

            "problem":
            "Poor performance hurts gameplay.",

            "recommendation":
            [
                "Profile rendering pipeline",
                "Optimize CPU/GPU bottlenecks"
            ],

            "expected_impact":
            "Improve player satisfaction."
        },

        "MATCHMAKING_RANK_BALANCE": {

            "problem":
            "Unfair matches reduce engagement.",

            "recommendation":
            [
                "Adjust matchmaking parameters",
                "Improve skill rating calibration"
            ],

            "expected_impact":
            "Increase competitive fairness."
        }
    }

    def get(
        self,
        issue_id
    ):

        return self.RECOMMENDATIONS.get(

            issue_id,

            {

                "problem":
                "Unknown",

                "recommendation":
                [
                    "Manual investigation required"
                ],

                "expected_impact":
                "Unknown"
            }
        )