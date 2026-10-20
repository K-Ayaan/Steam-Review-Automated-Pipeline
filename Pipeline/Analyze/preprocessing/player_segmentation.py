class PlayerSegmenter:

    def segment(
        self,
        playtime_hours
    ):

        if playtime_hours < 10:

            return "New Player"

        elif playtime_hours < 100:

            return "Casual Player"

        elif playtime_hours < 500:

            return "Core Player"

        return "Veteran"