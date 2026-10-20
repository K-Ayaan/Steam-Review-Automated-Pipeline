import re


class ReviewCompressor:

    def compress(
        self,
        review
    ):

        review = str(review)

        sentences = re.split(
            r'[.!?。\n]+',
            review
        )

        keywords = [

            "cheat",
            "hack",
            "vac",
            "match",
            "lag",
            "fps",
            "crash",
            "bug",
            "server",
            "subtick",
            "128",
            "toxic",
            "russian",

            "外挂",
            "作弊",
            "卡顿",
            "崩溃",
            "匹配",

            "чит",
            "читер",

            "hile"
        ]

        matches = []

        for sentence in sentences:

            lower = sentence.lower()

            if any(
                k in lower
                for k in keywords
            ):
                matches.append(
                    sentence.strip()
                )

        if matches:

            return " ".join(matches)

        return review[:1000]