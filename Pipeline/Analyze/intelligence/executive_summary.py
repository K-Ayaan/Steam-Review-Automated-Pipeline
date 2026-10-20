class ExecutiveSummary:

    def generate(
        self,
        report,
        health_scores,
        positive_reviews,
        total_reviews
    ):

        top_issues = sorted(

            report,

            key=lambda x: x["count"],

            reverse=True

        )[:5]

        summary = {

            "overall_health":
            health_scores["overall_health"],

            "review_score":
            positive_reviews,

            "top_issues": [

                issue["issue_id"]

                for issue in top_issues
            ]
        }

        return summary