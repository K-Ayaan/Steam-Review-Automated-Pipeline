import json
from pathlib import Path
from datetime import datetime

from database.campaign_repository import CampaignRepository


class PublishingLogger:

    def log(

        self,

        campaign_id,

        channel,

        status,

        message=""
    ):

        log_file = Path(
            "outputs/publishing_logs.json"
        )

        if log_file.exists():

            with open(

                log_file,

                "r",

                encoding="utf-8"

            ) as f:

                logs = json.load(f)

        else:

            logs = []

        logs.append({

            "timestamp":
            datetime.now().isoformat(),

            "campaign_id":
            campaign_id,

            "channel":
            channel,

            "status":
            status,

            "message":
            message
        })

        with open(

            log_file,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                logs,

                f,

                indent=4
            )

        CampaignRepository().log_publish(

            campaign_id,

            channel,

            status,

            message
        )