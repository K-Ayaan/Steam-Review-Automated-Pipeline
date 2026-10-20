'''Which audience performs best?
Which channel performs best?
Which campaign failed?
What should we scale?'''

class PublishingAnalytics:

    def analyze(

        self,

        campaigns
    ):

        if not campaigns:

            return {}

        best_campaign = max(

            campaigns,

            key=lambda x:

                x.get(
                    "clicks",
                    0
                )
        )

        worst_campaign = min(

            campaigns,

            key=lambda x:

                x.get(
                    "clicks",
                    0
                )
        )

        audience_scores = {}

        channel_scores = {}

        for campaign in campaigns:

            clicks = campaign.get(

                "clicks",

                0
            )

            audience = campaign.get(

                "audience",

                "Unknown"
            )

            channel = campaign.get(

                "channel",

                "Unknown"
            )

            audience_scores[
                audience
            ] = (

                audience_scores.get(
                    audience,
                    0
                )

                +

                clicks
            )

            channel_scores[
                channel
            ] = (

                channel_scores.get(
                    channel,
                    0
                )

                +

                clicks
            )

        best_audience = max(

            audience_scores,

            key=audience_scores.get
        )

        best_channel = max(

            channel_scores,

            key=channel_scores.get
        )

        return {

            "best_campaign":
            best_campaign,

            "worst_campaign":
            worst_campaign,

            "best_audience":
            best_audience,

            "best_channel":
            best_channel
        }