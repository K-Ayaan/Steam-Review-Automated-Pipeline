import json
from pathlib import Path


class CampaignMetricsSync:

    def sync(

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

        for campaign in campaigns:

            short_code = campaign.get(

                "short_code"
            )

            if short_code in links:

                campaign["clicks"] = (

                    links[short_code][

                        "clicks"
                    ]
                )

        return campaigns