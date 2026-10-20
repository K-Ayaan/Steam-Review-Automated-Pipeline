import json

from pathlib import Path


class ClickSync:

    def update(

        self,

        campaigns
    ):

        path = Path(

            "data/campaign_links.json"
        )

        if not path.exists():

            return campaigns

        with open(

            path,

            "r",

            encoding="utf-8"

        ) as f:

            links = json.load(f)

        campaign_clicks = {}

        for short_code, data in (

            links.items()
        ):

            campaign_id = (

                data["campaign_id"]
            )

            clicks = (

                data["clicks"]
            )

            campaign_clicks[

                campaign_id

            ] = clicks

        for campaign in campaigns:

            campaign_id = (

                campaign["campaign_id"]
            )

            campaign["clicks"] = (

                campaign_clicks.get(

                    campaign_id,

                    0
                )
            )

        return campaigns