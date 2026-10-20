from src.pagination import get_next_page_params
from src.steam_parser import extract_reviews
from src.storage import (save_checkpoint)
from bs4 import BeautifulSoup

def collect_reviews(
    client,
    app_id,
    max_pages
):

    all_reviews = []

    current_html = client.get(
        f"https://steamcommunity.com/app/{app_id}/reviews?p=1&browsefilter=toprated&filterLanguage=all"
    )

    soup = BeautifulSoup(current_html, "lxml")
    game_name = soup.select_one(
        ".apphub_AppName"
    ).get_text(strip=True)

    current_page = 1

    while True:

        print(
            f"Processing Page {current_page}"
        )

        reviews = extract_reviews(
            current_html,game_name
        )

        all_reviews.extend(reviews)

        print(
            f"Collected so far: "
            f"{len(all_reviews)}"
        )

        next_params = get_next_page_params(
            current_html
        )

        save_checkpoint(
            current_page,
            next_params
        )


        if not next_params:

            print(
                "No next page found."
            )

            break

        if current_page >= max_pages:

            print(
                "Reached max_pages limit."
            )

            break

        current_html = client.get_homecontent(app_id,next_params)

        # if current_page == 1:

        #     with open(
        #         "data/page2.html",
        #         "w",
        #         encoding="utf-8"
        #     ) as f:
        #         f.write(current_html)

        # if current_page == 2:

        #     with open(
        #         "data/page2.html",
        #         "w",
        #         encoding="utf-8"
        #     ) as f:
        #         f.write(current_html)
                

        current_page += 1

    return all_reviews