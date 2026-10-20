# class CampaignScorer:

#     def score(self, audience, campaign, health):
#         score = 50

#         score +=(len(audience["target_audiences"])*3)

#         score+= (len(campaign["promote"])*5)

#         score+= (health["overall_health" ]/5)

#         score -= ((100-health["review_health"] ) / 4)

#         return round(score, 1)


class CampaignScorer:

    def score(

        self,

        report,

        health_scores
    ):

        overall_health = health_scores.get(

            "overall_health",

            0
        )

        review_health = health_scores.get(

            "review_health",

            0
        )

        issue_health = health_scores.get(

            "issue_health",

            0
        )

        score = (

            overall_health * 0.5

            +

            review_health * 0.3

            +

            issue_health * 0.2
        )

        critical_count = len([

            issue

            for issue in report

            if issue[
                "severity"
            ] == "CRITICAL"
        ])

        high_count = len([

            issue

            for issue in report

            if issue[
                "severity"
            ] == "HIGH"
        ])

        score -= (

            critical_count * 5
        )

        score -= (

            high_count * 2
        )

        score = max(

            0,

            round(
                score,
                1
            )
        )

        # if score >= 85:

        #     readiness = "READY"

        # elif score >= 70:

        #     readiness = "GOOD"

        # elif score >= 55:

        #     readiness = "CAUTION"

        # else:

        #     readiness = "NOT READY"


        return score

        # return {

        #     "campaign_score":
        #     score,

        #     "readiness":
        #     readiness,

        #     "critical_issues":
        #     critical_count,

        #     "high_issues":
        #     high_count
        # }