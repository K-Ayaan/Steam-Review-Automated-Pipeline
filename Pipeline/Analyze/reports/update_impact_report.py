import json
from pathlib import Path


class UpdateImpactReport:

    def generate(self):

        all_runs = sorted(

            Path("outputs").glob(
                "run_*"
            ),

            reverse=True
        )

        valid_runs = []

        for run in all_runs:

            metadata_file = (
                run /
                "analysis_metadata.json"
            )

            issues_file = (
                run /
                "issues.json"
            )

            if (

                metadata_file.exists()

                and

                issues_file.exists()
            ):

                valid_runs.append(run)

        if len(valid_runs) < 2:

            return {}

        current_run = valid_runs[0]

        with open(

            current_run /
            "analysis_metadata.json",

            "r",

            encoding="utf-8"

        ) as f:

            current_metadata = json.load(f)

        current_game = current_metadata[
            "game_name"
        ]

        same_game_runs = []

        for run in valid_runs:

            with open(

                run /
                "analysis_metadata.json",

                "r",

                encoding="utf-8"

            ) as f:

                metadata = json.load(f)

            if (

                metadata[
                    "game_name"
                ]

                ==

                current_game

                and

                metadata.get(
                    "game_version",
                    "Unknown"
                ) != "Unknown"
            ):

                same_game_runs.append(

                    {

                        "run":
                        run,

                        "metadata":
                        metadata
                    }
                )

        if len(same_game_runs) < 2:

            print(
                f"Not enough runs for {current_game}"
            )

            return {}

        same_game_runs = sorted(

            same_game_runs,

            key=lambda x:

            x["metadata"][
                "review_end_date"
            ],

            reverse=True
        )

        current = same_game_runs[0]
        previous = same_game_runs[1]

        current_run = current["run"]
        previous_run = previous["run"]

        current_metadata = (
            current["metadata"]
        )

        previous_metadata = (
            previous["metadata"]
        )

        print(
            f"\nComparing:"
        )

        print(
            f"{previous_metadata['game_version']}"
        )

        print(
            f"VS"
        )

        print(
            f"{current_metadata['game_version']}"
        )

        with open(

            previous_run /
            "issues.json",

            "r",

            encoding="utf-8"

        ) as f:

            previous_issues = json.load(f)

        with open(

            current_run /
            "issues.json",

            "r",

            encoding="utf-8"

        ) as f:

            current_issues = json.load(f)

        previous_map = {

            issue["issue_id"]:
            issue["count"]

            for issue in previous_issues
        }

        current_map = {

            issue["issue_id"]:
            issue["count"]

            for issue in current_issues
        }

        all_issues = (

            set(previous_map.keys())

            |

            set(current_map.keys())
        )

        report = {

            "_comparison": {

                "game_name":
                current_game,

                "previous_version":
                previous_metadata[
                    "game_version"
                ],

                "current_version":
                current_metadata[
                    "game_version"
                ],

                "previous_period":

                f"{previous_metadata['review_start_date']}"

                f" -> "

                f"{previous_metadata['review_end_date']}",

                "current_period":

                f"{current_metadata['review_start_date']}"

                f" -> "

                f"{current_metadata['review_end_date']}"
            }
        }

        for issue in all_issues:

            before = previous_map.get(
                issue,
                0
            )

            after = current_map.get(
                issue,
                0
            )

            if before == 0:

                change = 100

            else:

                change = round(

                    (
                        (after - before)

                        /

                        before

                    ) * 100,

                    1
                )

            report[issue] = {

                "before":
                before,

                "after":
                after,

                "change_percent":
                change
            }

        return report