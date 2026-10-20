from datetime import datetime


class AnalysisMetadata:

    def generate(

        self,

        game_name,

        review_count,

        known_reviews,

        unknown_reviews,

        start_date,

        end_date,

        version="Unknown"

    ):

        return {

            "game_name":
            game_name,

            "analysis_date":
            datetime.now().strftime(
                "%Y-%m-%d"
            ),

            "review_start_date":
            str(start_date),

            "review_end_date":
            str(end_date),

            "game_version":
            version,

            "review_count":
            review_count,

            "known_reviews":
            known_reviews,

            "unknown_reviews":
            unknown_reviews
        }