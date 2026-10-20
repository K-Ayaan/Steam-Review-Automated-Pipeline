import os
import smtplib
from email.message import EmailMessage


REQUIRED_ENV = [

    "SMTP_HOST",

    "SMTP_FROM",

    "EMAIL_RECIPIENTS"
]


class EmailPublisher:

    def build_email(

        self,

        campaign
    ):

        creatives = campaign.get(

            "creatives",

            {}
        )

        body = (

            creatives.get("email_body")

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

        recipients = [

            r.strip()

            for r in os.getenv("EMAIL_RECIPIENTS", "").split(",")

            if r.strip()
        ]

        return {

            "subject":

            creatives.get(

                "email_subject"
            )

            or

            creatives.get(

                "headline",

                ""
            ),

            "body":
            f"{body}\n\n{cta}\n{link}".strip(),

            "from":
            os.getenv("SMTP_FROM", ""),

            "recipients":
            recipients
        }

    def publish(

        self,

        campaign,

        dry_run=True
    ):

        email = self.build_email(
            campaign
        )

        if dry_run:

            print(

                f"[DRY-RUN] Email to {email['recipients'] or '<EMAIL_RECIPIENTS>'}\n"

                f"  Subject: {email['subject']}\n"

                f"  Body: {email['body']}\n"
            )

            return {

                **email,

                "sent":
                False
            }

        missing = [

            name

            for name in REQUIRED_ENV

            if not os.getenv(name)
        ]

        if missing:

            raise ValueError(
                f"Missing SMTP env vars: {missing}"
            )

        message = EmailMessage()

        message["Subject"] = email["subject"]

        message["From"] = email["from"]

        message["To"] = ", ".join(
            email["recipients"]
        )

        message.set_content(
            email["body"]
        )

        port = int(
            os.getenv("SMTP_PORT") or "587"
        )

        # 465 = implicit SSL; other ports use STARTTLS

        smtp_class = (

            smtplib.SMTP_SSL

            if port == 465

            else smtplib.SMTP
        )

        with smtp_class(

            os.getenv("SMTP_HOST"),

            port,

            timeout=30

        ) as server:

            if (

                port != 465

                and

                (os.getenv("SMTP_USE_TLS") or "true").lower() == "true"
            ):

                server.starttls()

            if os.getenv("SMTP_USERNAME"):

                server.login(

                    os.getenv("SMTP_USERNAME"),

                    os.getenv("SMTP_PASSWORD", "")
                )

            server.send_message(
                message
            )

        return {

            **email,

            "sent":
            True
        }
