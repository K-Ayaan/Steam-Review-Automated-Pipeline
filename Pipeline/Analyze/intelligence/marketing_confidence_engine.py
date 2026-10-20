class MarketingConfidenceEngine:

    def calculate(

        self,

        health_scores,

        report
    ):

        score = 100

        score -= (

            100

            -

            health_scores[
                "overall_health"
            ]
        )

        high_count = len([

            issue

            for issue in report

            if issue[
                "severity"
            ] == "HIGH"
        ])

        critical_count = len([

            issue

            for issue in report

            if issue[
                "severity"
            ] == "CRITICAL"
        ])

        score -= (

            high_count * 5
        )

        score -= (

            critical_count * 10
        )

        score = max(
            score,
            0
        )

        return {

            "marketing_confidence":
            round(score, 1),

            "recommendation":

            "LAUNCH"

            if score >= 70

            else

            "FIX ISSUES FIRST"
        }