import json
from pathlib import Path


class TrendAnalyzer:

    def generate(self):

        runs = sorted(

            Path("outputs").glob(
                "run_*"
            )
        )

        history = []

        for run in runs:

            metadata_file = (
                run /
                "analysis_metadata.json"
            )

            health_file = (
                run /
                "health_scores.json"
            )

            if (

                not metadata_file.exists()

                or

                not health_file.exists()
            ):

                continue

            with open(

                metadata_file,

                "r",

                encoding="utf-8"

            ) as f:

                metadata = json.load(f)

            with open(

                health_file,

                "r",

                encoding="utf-8"

            ) as f:

                health = json.load(f)

            history.append({

                "version":

                metadata.get(
                    "game_version",
                    "Unknown"
                ),

                "overall_health":

                health.get(
                    "overall_health",
                    0
                ),

                "review_health":

                health.get(
                    "review_health",
                    0
                ),

                "known_reviews":

                metadata.get(
                    "known_reviews",
                    0
                ),

                "unknown_reviews":

                metadata.get(
                    "unknown_reviews",
                    0
                )
            })

        return history