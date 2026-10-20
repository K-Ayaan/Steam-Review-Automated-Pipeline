import os

from publishers.discord_publisher import (
    DiscordPublisher
)

from config.discord_config import (
    DISCORD_WEBHOOK_URL
)

from services.publishing_logger import (
    PublishingLogger
)

from publishers.reddit_publisher import (
    RedditPublisher
)

from publishers.email_publisher import (
    EmailPublisher
)

class Publisher:

    def __init__(self):

        self.discord = (
            DiscordPublisher()
        )

        self.logger = (
            PublishingLogger()
        )

        self.reddit = (
            RedditPublisher()
        )

        self.email = (
            EmailPublisher()
        )

    def publish(

        self,

        campaign,

        dry_run=True
    ):

        # dry_run (default) prints what would be sent;
        # nothing leaves the machine and nothing is logged.

        platform = campaign.get(

            "platform",

            "discord"
        )

        if platform == "discord":

            if dry_run:

                creatives = campaign.get(
                    "creatives",
                    {}
                )

                print(

                    f"[DRY-RUN] Discord webhook\n"

                    f"  **{creatives.get('headline', '')}**\n"

                    f"  {creatives.get('ad_copy', '')}\n"

                    f"  {creatives.get('cta', '')}\n"

                    f"  {campaign.get('tracking_url', '')}\n"
                )

                return True

            success = self.discord.publish(

                os.getenv(
                    "DISCORD_WEBHOOK_URL",
                    DISCORD_WEBHOOK_URL
                ),

                campaign
            )

            self.logger.log(

                campaign_id=
                campaign["campaign_id"],

                channel=
                campaign["channel"],

                status=
                "SUCCESS"

                if success

                else

                "FAILED",

                message=
                (
                    f"Audience={campaign['audience']} | "
                    f"Headline={campaign.get('headline','')}"
                )

            )

            return success

        if platform == "reddit":

            try:

                result = (

                    self.reddit.publish(

                        campaign,

                        dry_run=dry_run
                    )
                )

            except ValueError as e:

                # Missing REDDIT_* config: skip, don't abort the batch

                print(
                    f"Reddit skipped for {campaign['campaign_id']}: {e}"
                )

                return False

            except Exception as e:

                self.logger.log(

                    campaign_id=
                    campaign["campaign_id"],

                    channel=
                    campaign["channel"],

                    status=
                    "FAILED",

                    message=
                    str(e)
                )

                return False

            if not dry_run:

                self.logger.log(

                    campaign_id=
                    campaign["campaign_id"],

                    channel=
                    campaign["channel"],

                    status=
                    "SUCCESS",

                    message=
                    f"post_id={result.get('post_id')} | {result.get('url')}"
                )

            return result

        if platform == "email":

            try:

                result = (

                    self.email.publish(

                        campaign,

                        dry_run=dry_run
                    )
                )

            except ValueError as e:

                print(
                    f"Email skipped for {campaign['campaign_id']}: {e}"
                )

                return False

            except Exception as e:

                self.logger.log(

                    campaign_id=
                    campaign["campaign_id"],

                    channel=
                    campaign["channel"],

                    status=
                    "FAILED",

                    message=
                    str(e)
                )

                return False

            if not dry_run:

                self.logger.log(

                    campaign_id=
                    campaign["campaign_id"],

                    channel=
                    campaign["channel"],

                    status=
                    "SUCCESS",

                    message=
                    f"to={','.join(result['recipients'])}"
                )

            return result

        return False
