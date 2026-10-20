import json
from pathlib import Path


class TrendAnalyzer:

    def load_health_scores(
        self,
        outputs_dir="outputs"
    ):

        runs = []

        outputs_path = Path(
            outputs_dir
        )

        if not outputs_path.exists():

            return []

        for run_dir in sorted(
            outputs_path.iterdir()
        ):

            health_file = (
                run_dir /
                "health_scores.json"
            )

            if health_file.exists():

                with open(
                    health_file,
                    "r"
                ) as f:

                    data = json.load(f)

                runs.append({

                    "run":
                    run_dir.name,

                    "scores":
                    data
                })

        return runs
    

    def compare_latest_runs(
        self,
        outputs_dir="outputs"
    ):

        runs = self.load_health_scores(
            outputs_dir
        )

        if len(runs) < 2:

            return None

        previous = runs[-2]

        current = runs[-1]

        result = {}

        for metric in current["scores"]:

            current_value = (
                current["scores"][metric]
            )

            previous_value = (
                previous["scores"][metric]
            )

            delta = (
                current_value
                - previous_value
            )

            if delta > 0:

                status = "IMPROVING"

            elif delta < 0:

                status = "DECLINING"

            else:

                status = "UNCHANGED"

            result[metric] = {

                "previous":
                previous_value,

                "current":
                current_value,

                "delta":
                round(delta, 2),

                "status":
                status
            }

        return result