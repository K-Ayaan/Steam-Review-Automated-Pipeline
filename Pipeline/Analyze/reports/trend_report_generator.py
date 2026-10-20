import json
from pathlib import Path


class TrendReportGenerator:

    def generate(self):

        outputs = Path("outputs")

        runs = sorted(

            outputs.glob("run_*")

        )

        trend_data = {}

        for run in runs:

            issues_file = (

                run /

                "issues.json"
            )

            if not issues_file.exists():

                continue

            run_name = run.name

            with open(

                issues_file,

                "r",

                encoding="utf-8"

            ) as f:

                issues = json.load(f)

            for issue in issues:

                issue_id = issue[
                    "issue_id"
                ]

                if issue_id not in trend_data:

                    trend_data[
                        issue_id
                    ] = {}

                trend_data[
                    issue_id
                ][run_name] = (

                    issue["count"]
                )
        return trend_data