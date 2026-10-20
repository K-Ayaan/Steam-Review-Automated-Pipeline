from pathlib import Path
from datetime import datetime


class RunManager:

    def create_run_folder(self):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        run_dir = Path(
            "outputs"
        ) / f"run_{timestamp}"

        run_dir.mkdir(

            parents=True,

            exist_ok=True
        )

        return run_dir
    