class GameHealthScore:

    def calculate(
        self,
        report,
        known_reviews,
        positive_reviews,
        total_reviews
    ):

        scores = {

            "anti_cheat_health": 100,

            "matchmaking_health": 100,

            "community_health": 100,

            "economy_health": 100,

            "technical_health": 100,

            "multiplayer_health": 100,

            "gameplay_health": 100,

            "horror_health": 100,

            "ux_health": 100
        }

        severity_penalties = {

            "LOW": 5,

            "MEDIUM": 15,

            "HIGH": 30,

            "CRITICAL": 50
        }

        for issue in report:

            issue_id = issue["issue_id"]

            severity = issue["severity"]

            count = issue["count"]

            base_penalty = (
                severity_penalties.get(
                    severity,
                    0
                )
            )

            frequency_multiplier = min(

                count / max(
                    known_reviews,
                    1
                ),

                1.0
            )

            penalty = (

                base_penalty

                +

                (
                    frequency_multiplier
                    * 15
                )

            )

            if issue_id in [

                "BUGS",
                "CRASHES",
                "PERFORMANCE_FPS"

            ]:

                scores[
                    "technical_health"
                ] -= penalty

            elif issue_id in [

                "MULTIPLAYER_CONNECTIVITY"

            ]:

                scores[
                    "multiplayer_health"
                ] -= penalty

            elif issue_id in [

                "GAMEPLAY_CLARITY",
                "GAMEPLAY_BALANCE",
                "CONTENT_REQUESTS",
                "REPLAYABILITY"

            ]:

                scores[
                    "gameplay_health"
                ] -= penalty

            elif issue_id in [

                "HORROR_EFFECTIVENESS"

            ]:

                scores[
                    "horror_health"
                ] -= penalty

            elif issue_id in [

                "UI_UX_PROBLEMS",
                "LOCALIZATION"

            ]:

                scores[
                    "ux_health"
                ] -= penalty

            elif issue_id in [

                "COMMUNITY_TOXICITY"

            ]:

                scores[
                    "community_health"
                ] -= penalty

            elif issue_id in [

                "ANTI_CHEAT_CHEATERS",
                "ANTI_CHEAT_VAC_VERIFICATION"

            ]:

                scores[
                    "anti_cheat_health"
                ] -= penalty

            elif issue_id in [

                "MATCHMAKING",
                "REGIONAL_MATCHMAKING"

            ]:

                scores[
                    "matchmaking_health"
                ] -= penalty

            elif issue_id in [

                "SKIN_ECONOMY"

            ]:

                scores[
                    "economy_health"
                ] -= penalty

        for key in scores:

            scores[key] = round(

                max(
                    0,
                    min(
                        100,
                        scores[key]
                    )
                ),

                1
            )

        SEVERITY_PENALTY = {

            "CRITICAL": 25,

            "HIGH": 15,

            "MEDIUM": 8,

            "LOW": 3
        }

        total_penalty = 0

        total_mentions = 0

        for issue in report:

            mentions = issue["count"]

            penalty = SEVERITY_PENALTY.get(

                issue["severity"],

                0
            )

            total_penalty += (

                penalty

                * mentions
            )

            total_mentions += mentions

        average_penalty = (

            total_penalty

            /

            max(
                total_mentions,
                1
            )
        )

        issue_health = round(

            max(

                0,

                100 - average_penalty
            ),

            1
        )

        review_health = round(

            (
                positive_reviews

                /

                max(
                    total_reviews,
                    1
                )
            )

            * 100,

            1
        )

        subsystem_health = round(

            (

                scores["anti_cheat_health"]

                +

                scores["matchmaking_health"]

                +

                scores["community_health"]

                +

                scores["economy_health"]

                +

                scores["technical_health"]

                +

                scores["multiplayer_health"]

                +

                scores["gameplay_health"]

                +

                scores["horror_health"]

                +

                scores["ux_health"]

            )

            / 9,

            1
        )

        scores[
            "review_health"
        ] = review_health

        scores[
            "issue_health"
        ] = issue_health

        scores[
            "overall_health"
        ] = round(

            (

                review_health
                * 0.5

            )

            +

            (

                issue_health
                * 0.2

            )

            +

            (

                subsystem_health * 0.3

            ),

            1
        )

        return scores