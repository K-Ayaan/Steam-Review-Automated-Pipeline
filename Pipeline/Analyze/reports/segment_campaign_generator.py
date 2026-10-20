class SegmentCampaignGenerator:

    def generate(

        self,

        audience_report,

        campaign_report
    ):

        campaigns = []

        promote = campaign_report.get(

            "promote",

            []
        )

        platforms = [

            "reddit",

            "discord",

            "email"
        ]

        for audience in audience_report.get(

            "target_audiences",

            []
        ):

            for platform in platforms:

                campaigns.append({

                    "audience":
                    audience,

                    "platform":
                    platform,

                    "channel":
                    platform.title(),

                    "promote":
                    promote
                })

        return campaigns