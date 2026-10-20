RETENTION_WEIGHTS = {

    "REPLAYABILITY": 1.0,

    "CONTENT_REQUESTS": 0.9,

    "COMMUNITY_TOXICITY": 0.8,

    "MATCHMAKING_RANK_BALANCE": 0.8,

    "MATCHMAKING_REGIONAL": 0.7,

    "ANTI_CHEAT_CHEATERS": 0.9,

    "SERVER_CONNECTIVITY": 0.8,

    "MULTIPLAYER_CONNECTIVITY": 0.8,

    "BUGS": 0.6,

    "CRASHES": 0.7,

    "PERFORMANCE_FPS": 0.7,

    "OPTIMIZATION": 0.7,

    "UI_UX_PROBLEMS": 0.4,

    "LOCALIZATION": 0.2
}

SEGMENT_REVENUE_MULTIPLIER = {

    "Core Player": 1.0,

    "Veteran": 0.9,

    "Casual Player": 0.6,

    "New Player": 0.4
}

class ReviewImpactPredictor:

    def predict(

        self,

        issue
    ):

        issue_id = issue[
            "issue_id"
        ]

        count = issue[
            "count"
        ]

        impact_score = issue[
            "impact_score"
        ]

        severity = issue[
            "severity"
        ]

        player_segment = issue.get(

            "top_player_segment",

            "Casual Player"
        )

        severity_multiplier = {

            "CRITICAL": 1.0,

            "HIGH": 0.75,

            "MEDIUM": 0.5,

            "LOW": 0.25
        }

        review_risk = round(

            (

                count

                *

                impact_score

                *

                severity_multiplier.get(

                    severity,

                    0.25
                )

            )

            / 1000,

            2
        )

        retention_weight = (

            RETENTION_WEIGHTS.get(

                issue_id,

                0.5
            )
        )

        retention_risk = round(

            review_risk

            *

            retention_weight,

            2
        )

        segment_multiplier = (

            SEGMENT_REVENUE_MULTIPLIER.get(

                player_segment,

                0.6
            )
        )

        revenue_risk = round(

            retention_risk

            *

            segment_multiplier,

            2
        )

        marketing_safe = not (

            severity

            in [

                "CRITICAL",

                "HIGH"
            ]

            and

            revenue_risk > 2
        )

        return {

            "issue_id":
            issue_id,

            "severity":
            severity,

            "review_risk":
            review_risk,

            "retention_risk":
            retention_risk,

            "revenue_risk":
            revenue_risk,

            "marketing_safe":
            marketing_safe,

            "top_player_segment":
            player_segment
        }