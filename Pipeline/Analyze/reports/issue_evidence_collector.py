class IssueEvidenceCollector:

    def collect(

        self,

        issue_id,

        reviews,

        max_reviews=5

    ):

        evidence = []

        count = 0

        for review in reviews:

            issues = review["issues"]

            if issue_id in issues:

                evidence.append({

                    "impact_score":
                    review["impact_score"],

                    "helpful_count":
                    review["helpful_count"],

                    "review_text":
                    review["review_text"]
                })

                count += 1

            if count >= max_reviews:

                break

        evidence = sorted(

            evidence,

            key=lambda x: (

                x["impact_score"],

                x["helpful_count"]

            ),

            reverse=True
        )

        return evidence