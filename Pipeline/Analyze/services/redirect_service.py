import json

from pathlib import Path

from fastapi import FastAPI

from fastapi.responses import RedirectResponse


app = FastAPI()


@app.get("/r/{short_code}")

def redirect(

    short_code: str
):

    path = Path(

        "data/campaign_links.json"
    )

    if not path.exists():

        return {

            "error":
            "No links found"
        }

    with open(

        path,

        "r",

        encoding="utf-8"

    ) as f:

        links = json.load(f)

    if short_code not in links:

        return {

            "error":
            "Invalid code"
        }

    links[short_code][

        "clicks"

    ] += 1

    with open(

        path,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            links,

            f,

            indent=4
        )

    return RedirectResponse(

        links[short_code][

            "destination_url"
        ]
    )
