import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent)
)

from src.request_client import SteamRequestClient

from src.steam_collector import (
    collect_reviews
)

from src.storage import save_reviews


APP_ID = 3297310

#CS2: 730
#TheCursedHour: 3297310
#KtrlSmash: 4223440
#Valheim: 892970
#Escape The Backrooms: 1943950
#Marvel Rivals:2767030

OUTPUT_FILE = (

    Path(__file__).resolve().parent.parent

    / "Analyze" / "data" / "reviews.csv"
)


def scrape(

    app_id,

    output_path=OUTPUT_FILE,

    max_pages=20,

    max_reviews=None
):

    client = SteamRequestClient()

    reviews = collect_reviews(
        client,
        app_id,
        max_pages = max_pages
    )

    if max_reviews:

        reviews = reviews[:max_reviews]

    print(
        f"Collected {len(reviews)} reviews"
    )

    save_reviews(
        reviews,
        str(output_path)
    )

    return reviews


if __name__ == "__main__":

    scrape(
        int(sys.argv[1]) if len(sys.argv) > 1 else APP_ID
    )
