import os
from pathlib import Path


ANALYZE_ROOT = Path(__file__).resolve().parent.parent

REPO_ROOT = ANALYZE_ROOT.parent.parent


def load_env():

    # Load KEY=VALUE lines from .env without
    # overriding variables already set in the shell.

    for env_file in [

        ANALYZE_ROOT / ".env",

        REPO_ROOT / ".env"
    ]:

        if not env_file.exists():

            continue

        with open(

            env_file,

            "r",

            encoding="utf-8"

        ) as f:

            for line in f:

                line = line.strip()

                if (

                    not line

                    or

                    line.startswith("#")

                    or

                    "=" not in line
                ):

                    continue

                key, value = line.split(
                    "=",
                    1
                )

                value = value.strip().strip(
                    "\"'"
                )

                # Blank placeholders keep code defaults

                if not value:

                    continue

                os.environ.setdefault(

                    key.strip(),

                    value
                )
