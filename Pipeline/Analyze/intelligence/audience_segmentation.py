class AudienceSegmentation:

    def generate(

        self,

        report

    ):

        strengths = []

        weaknesses = []

        audiences = set()

        for issue in report:

            issue_id = issue["issue_id"]

            count = issue["count"]

            signal_type = issue.get(

                "signal_type",

                "negative"
            )

            if signal_type == "positive":

                strengths.append(

                    issue_id
                )

            else:

                weaknesses.append(

                    issue_id
                )

        if (

            "HORROR_EXPERIENCE"

            in strengths

            or

            "IMMERSION"

            in strengths
        ):

            audiences.add(

                "Horror Fans"
            )

        if (

            "MULTIPLAYER_FUN"

            in strengths

            or

            "MULTIPLAYER_CONNECTIVITY"

            in weaknesses
        ):

            audiences.add(

                "Co-op Players"
            )

        if (

            "REPLAYABILITY"

            in strengths
        ):

            audiences.add(

                "Hardcore Gamers"
            )

        return {

            "game_name":

                report[0].get(
                    "game_name",
                    "Unknown"
                )

                if report

                else "Unknown",

            "strengths":
                strengths,

            "weaknesses":
                weaknesses,

            "target_audiences":
                list(audiences)
        }