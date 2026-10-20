class ReviewFilter:

    def should_skip(

        self,

        review
    ):

        review = str(
            review
        ).lower()

        skin_jokes = [

            "刀会转",
            "knife",
            "开箱",
            "库存",
            "inventory",
            "dragon lore",
            "龙狙"
        ]

        for phrase in skin_jokes:

            if phrase.lower() in review:

                return True

        skip_phrases = [

            "steamcommunity.com",

            "inventory",

            "great memories",

            "college days"
        ]

        for phrase in skip_phrases:

            if phrase in review:

                return True

        return False