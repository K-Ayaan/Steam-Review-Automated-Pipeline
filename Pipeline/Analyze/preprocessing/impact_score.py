class ImpactScoreCalculator:

    def calculate(

        self,

        helpful_count,

        review_length,

        playtime_hours

    ):

        score = 0

        score += (
            helpful_count * 3
        )

        score += (
            review_length * 0.1
        )

        score += (
            playtime_hours * 0.5
        )

        return round(score)