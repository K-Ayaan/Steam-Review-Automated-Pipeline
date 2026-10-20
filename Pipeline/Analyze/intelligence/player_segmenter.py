class PlayerSegmenter:

    def segment(

        self,

        hours_played

    ):

        try:

            hours_played = str(
                hours_played
            )

            hours_played = (

                hours_played

                .replace(
                    "h",
                    ""
                )

                .strip()
            )

            hours_played = float(
                hours_played
            )

        except:

            hours_played = 0

        if hours_played < 10:

            return "New Player"

        if hours_played < 100:

            return "Casual Player"

        if hours_played < 500:

            return "Core Player"

        return "Veteran Player"