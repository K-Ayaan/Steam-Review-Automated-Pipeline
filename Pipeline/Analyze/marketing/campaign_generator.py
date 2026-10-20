class CampaignGenerator:

    def generate(

        self,

        marketing_report

    ):

        audiences = marketing_report.get(

            "target_audiences",

            []
        )

        strengths = marketing_report.get(

            "angles",

            []
        )

        avoid = marketing_report.get(

            "avoid",

            []
        )

        campaign = {

            "target_audience":

                audiences,

            "promote":

                strengths,

            "avoid":

                avoid,

            "recommended_channels": [],

            "channel_platforms": {}
        }

        if "Horror Fans" in audiences:

            channel = (
                "YouTube Horror Creators"
            )

            campaign[
                "recommended_channels"
            ].append(
                channel
            )

            campaign[
                "channel_platforms"
            ][channel] = (
                "youtube"
            )

        if "Co-op Players" in audiences:

            channel = (
                "Discord Communities"
            )

            campaign[
                "recommended_channels"
            ].append(
                channel
            )

            campaign[
                "channel_platforms"
            ][channel] = (
                "discord"
            )

        if "Competitive Players" in audiences:

            channel = (
                "Reddit Gaming Communities"
            )

            campaign[
                "recommended_channels"
            ].append(
                channel
            )

            campaign[
                "channel_platforms"
            ][channel] = (
                "reddit"
            )

        return campaign