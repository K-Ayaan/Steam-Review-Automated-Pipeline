import json
from pathlib import Path


class CampaignManager:

    def load(

        self,

        run_dir
    ):

        path = (

            run_dir /

            "segment_campaigns.json"
        )

        # print(
        #     "Loading campaigns:",
        #     path
        # )

        if not path.exists():

            return []

        with open(

            path,

            "r",

            encoding="utf-8"

        ) as f:

            return json.load(f)
        

    def save(

        self,

        run_dir,

        campaigns
    ):

        with open(

            run_dir /

            "segment_campaigns.json",

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                campaigns,

                f,

                indent=4
            )

        # print(
        #     "Saving campaigns:",
        #     run_dir / "campaigns.json"
        # )