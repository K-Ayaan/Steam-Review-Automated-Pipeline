class CampaignPlanner:

    def generate(

        self,

        campaign_report,

        audience_report,

        marketing_confidence

    ):

        confidence = marketing_confidence[
            "marketing_confidence"
        ]

        plan = []

        channels = campaign_report.get(
            "recommended_channels",
            []
        )

        audiences = audience_report.get(
            "target_audiences",
            []
        )

        for idx, audience in enumerate(

            audiences

        ):

            channel = (

                channels[
                    idx % len(channels)
                ]

                if channels

                else

                "General"
            )

            if confidence >= 80:

                priority = "HIGH"

            elif confidence >= 60:

                priority = "MEDIUM"

            else:

                priority = "LOW"

            plan.append({

                "audience":
                audience,

                "channel":
                channel,

                "priority":
                priority
            })

        return plan