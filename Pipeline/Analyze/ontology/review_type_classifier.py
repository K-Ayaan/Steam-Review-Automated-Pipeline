class ReviewTypeClassifier:

    def classify(
        self,
        text
    ):

        text = str(
            text
        ).lower()

        if (
            "https://steamcommunity"
            in text
        ):

            return "PROFILE_LINK"

        if (
            "product received for free"
            in text
        ):

            return "FREE_PRODUCT"

        if len(
            text.split()
        ) > 300:

            return "LONG_STORY"

        if len(
            text.split()
        ) < 15:

            return "SHORT_REACTION"

        return "GENERAL"