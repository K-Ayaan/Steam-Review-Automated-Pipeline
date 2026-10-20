class CampaignAnalytics:

    def analyze(

        self,

        campaigns
    ):

        results = []

        for campaign in campaigns:

            impressions = campaign.get(

                "impressions",

                0
            )

            clicks = campaign.get(

                "clicks",

                0
            )

            visits = campaign.get(

                "visits",

                0
            )

            wishlists = campaign.get(

                "wishlists",

                0
            )

            downloads = campaign.get(

                "downloads",

                0
            )

            ctr = 0

            wishlist_rate = 0

            download_rate = 0

            if impressions > 0:

                ctr = round(

                    clicks

                    /

                    impressions

                    * 100,

                    2
                )

            if visits > 0:

                wishlist_rate = round(

                    wishlists

                    /

                    visits

                    * 100,

                    2
                )

                download_rate = round(

                    downloads

                    /

                    visits

                    * 100,

                    2
                )

            results.append({

                **campaign,

                "ctr":
                ctr,

                "wishlist_rate":
                wishlist_rate,

                "download_rate":
                download_rate
            })

        return results