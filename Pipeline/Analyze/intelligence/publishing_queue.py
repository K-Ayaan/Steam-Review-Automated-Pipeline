class PublishingQueue:

    def get_ready_campaigns(

        self,

        campaigns
    ):

        return [

            campaign

            for campaign in campaigns

            if campaign.get(

                "status"

            ) in [

                "APPROVED",

                "PUBLISHED"
            ]
        ]