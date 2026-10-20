from intelligence.campaign_scorer import (
    CampaignScorer
)


class CampaignRankingGenerator:

    def __init__(self):

        self.scorer = (
            CampaignScorer()
        )

    def generate(

        self,

        report,

        health
    ):

        score = (

            self.scorer.score(

                report,

                health
            )
        )

        return {

            "campaign_score":
            score,

            "recommendation":

            "Launch"

            if score >= 70

            else

            "Improve First"
        }