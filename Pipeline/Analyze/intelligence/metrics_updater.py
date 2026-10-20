import pandas as pd


class MetricsUpdater:

    def update(

        self,

        campaigns,

        metrics_df
    ):

        for campaign in campaigns:

            audience = campaign[
                "audience"
            ]

            channel = campaign[
                "channel"
            ]

            rows = metrics_df[

                (metrics_df["audience"] == audience)

                &

                (metrics_df["channel"] == channel)
            ]

            if len(rows) == 0:

                continue

            latest = rows.iloc[-1]

            campaign["impressions"] = int(

                latest["impressions"]
            )

            campaign["clicks"] = int(

                latest["clicks"]
            )

            campaign["visits"] = int(

                latest["visits"]
            )

            campaign["wishlists"] = int(

                latest["wishlists"]
            )

            campaign["downloads"] = int(

                latest["downloads"]
            )

        return campaigns