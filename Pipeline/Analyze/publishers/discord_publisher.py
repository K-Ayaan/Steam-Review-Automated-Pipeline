import requests


class DiscordPublisher:

    def publish(

        self,

        webhook_url,

        campaign
    ):

        creatives = campaign.get(

            "creatives",

            {}
        )

        headline = creatives.get(

            "headline",

            ""
        )

        ad_copy = creatives.get(

            "ad_copy",

            ""
        )

        tracking_url = campaign.get(

            "tracking_url",

            ""
        )

        cta = creatives.get(

            "cta",

            ""
        )

        message = f"""
**{headline}**

{ad_copy}

{cta}

{tracking_url}
"""

        response = requests.post(

            webhook_url,

            json={

                "content":
                message
            }
        )

        return response.status_code == 204