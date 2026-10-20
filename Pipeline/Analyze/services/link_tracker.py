import json
import secrets
from pathlib import Path


class LinkTracker:

    def generate(

        self,

        campaign_id,

        destination_url
    ):

        short_code = (

            secrets.token_urlsafe(6)
        )

        path = Path(

            "data/campaign_links.json"
        )

        path.parent.mkdir(

            exist_ok=True
        )

        if path.exists():

            with open(

                path,

                "r",

                encoding="utf-8"

            ) as f:

                links = json.load(f)

        else:

            links = {}

        links[short_code] = {

            "campaign_id":
            campaign_id,

            "destination_url":
            destination_url,

            "clicks":
            0
        }

        with open(

            path,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                links,

                f,

                indent=4
            )

        return short_code