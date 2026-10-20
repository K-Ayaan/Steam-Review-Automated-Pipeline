class CampaignRanker:

    def rank(

        self,

        marketing_report,

        health_scores

    ):

        campaigns = []

        for audience in marketing_report[
            "target_audiences"
        ]:

            score = 0

            if audience == \
                "Competitive Players":

                score += 10

            if audience == \
                "Friend Groups":

                score += 8

            if audience == \
                "Co-op Players":

                score += 8

            score += (

                health_scores[
                    "overall_health"
                ] / 10
            )

            campaigns.append({

                "audience":
                audience,

                "score":
                round(score, 1)
            })

        campaigns.sort(

            key=lambda x:
            x["score"],

            reverse=True
        )

        return campaigns