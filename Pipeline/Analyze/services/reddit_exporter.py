import pandas as pd


class RedditExporter:

    def export(

        self,

        campaigns,

        output_path
    ):

        rows = []

        for campaign in campaigns:

            creatives = campaign.get(

                "creatives",

                {}
            )

            rows.append({

                "title":

                creatives.get(

                    "headline",

                    ""
                ),

                "body":

                creatives.get(

                    "reddit_post",

                    ""
                ),

                "tracked_url":

                campaign.get(

                    "tracked_url",

                    ""
                )
            })

        pd.DataFrame(

            rows

        ).to_csv(

            output_path,

            index=False
        )