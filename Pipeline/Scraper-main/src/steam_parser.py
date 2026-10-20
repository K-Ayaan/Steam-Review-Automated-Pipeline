import re
from datetime import datetime

from bs4 import BeautifulSoup


def extract_reviews(html, game_name):

    soup = BeautifulSoup(html, "lxml")

    review_blocks = soup.select(
        ".apphub_UserReviewCardContent"
    )

    reviews = []

    for review in review_blocks:

        review_data = {}

        review_data["game_name"] = (
            game_name
        )

        title = review.select_one(".title")

        review_data["recommendation"] = (
            title.get_text(strip=True)
            if title
            else None
        )

        hours = review.select_one(".hours")

        review_data["hours_played"] = (
            hours.get_text(strip=True)
            if hours
            else None
        )

        date = review.select_one(".date_posted")

        date_text = date.get_text(strip=True).replace("Posted:", "").strip()
        date_text = date_text.replace(",", "")

        parts = date_text.split()

        if len(parts) == 2:
            parts.append(str(datetime.now().year))

        date_text = " ".join(parts)

        for fmt in ("%d %B %Y", "%B %d %Y"):
            try:
                review_data["date_posted"] = datetime.strptime(date_text, fmt).date()
                break
            except ValueError:
                pass
        else:
            raise ValueError(f"Could not parse date: {date_text}")


        text_container = review.select_one(
            ".apphub_CardTextContent"
        )

        if text_container:

            date_div = text_container.select_one(
                ".date_posted"
            )

            if date_div:
                date_div.extract()

            review_data["review_text"] = text_container.get_text(
                separator=" ",
                strip=True
            )

        helpful_div = review.select_one(
            ".found_helpful"
        )

        helpful_count = 0
        funny_count = 0

        if helpful_div:

            helpful_text = helpful_div.get_text(
                " ",
                strip=True
            )

            helpful_match = re.search(
                r"(\d+)\s+people found this review helpful",
                helpful_text
            )

            funny_match = re.search(
                r"(\d+)\s+people found this review funny",
                helpful_text
            )

            if helpful_match:
                helpful_count = int(
                    helpful_match.group(1)
                )

            if funny_match:
                funny_count = int(
                    funny_match.group(1)
                )

        review_data["helpful_count"] = helpful_count
        review_data["funny_count"] = funny_count

        reviews.append(review_data)

    return reviews