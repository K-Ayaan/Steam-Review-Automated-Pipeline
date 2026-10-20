class BusinessImpactEngine:

    def calculate(
        self,
        issue
    ):

        score = 0

        score += (
            issue["impact_score"] / 1000
        )

        score += (
            issue["helpful_count"] / 500
        )

        score += (
            issue["count"] * 2
        )

        if (
            issue["top_player_segment"]
            == "Veteran"
        ):

            score += 50

        if score >= 300:

            return "EXTREME"

        if score >= 150:

            return "HIGH"

        if score >= 75:

            return "MEDIUM"

        return "LOW"