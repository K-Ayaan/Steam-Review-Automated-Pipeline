import os

import praw


REQUIRED_ENV = [

    "REDDIT_CLIENT_ID",

    "REDDIT_CLIENT_SECRET",

    "REDDIT_USERNAME",

    "REDDIT_PASSWORD",

    "REDDIT_SUBREDDIT"
]


class RedditPublisher:

    def build_post(

        self,

        campaign
    ):

        creatives = campaign.get(

            "creatives",

            {}
        )

        body = (

            creatives.get("reddit_post")

            or

            creatives.get("ad_copy", "")
        )

        cta = creatives.get(
            "cta",
            ""
        )

        link = campaign.get(
            "tracking_url",
            ""
        )

        return {

            "title":

            creatives.get(

                "reddit_title"
            )

            or

            creatives.get(

                "headline",

                ""
            ),

            "body":
            f"{body}\n\n{cta}\n\n{link}".strip(),

            "tracked_url":

            campaign.get(

                "tracked_url",

                ""
            ),

            "subreddit":
            os.getenv("REDDIT_SUBREDDIT", "")
        }

    def publish(

        self,

        campaign,

        dry_run=True
    ):

        post = self.build_post(
            campaign
        )

        if dry_run:

            print(

                f"[DRY-RUN] Reddit r/{post['subreddit'] or '<REDDIT_SUBREDDIT>'}\n"

                f"  Title: {post['title']}\n"

                f"  Body: {post['body']}\n"
            )

            return {

                **post,

                "posted":
                False
            }

        missing = [

            name

            for name in REQUIRED_ENV

            if not os.getenv(name)
        ]

        if missing:

            raise ValueError(
                f"Missing Reddit env vars: {missing}"
            )

        reddit = praw.Reddit(

            client_id=os.getenv("REDDIT_CLIENT_ID"),

            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),

            username=os.getenv("REDDIT_USERNAME"),

            password=os.getenv("REDDIT_PASSWORD"),

            user_agent=os.getenv(

                "REDDIT_USER_AGENT",

                "steam-ad-review/1.0"
            )
        )

        submission = reddit.subreddit(

            post["subreddit"]

        ).submit(

            title=post["title"],

            selftext=post["body"]
        )

        return {

            **post,

            "posted":
            True,

            "post_id":
            submission.id,

            "url":
            f"https://www.reddit.com{submission.permalink}"
        }
