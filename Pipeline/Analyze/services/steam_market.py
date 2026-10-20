import json
import re
from datetime import datetime
from pathlib import Path

import requests


CACHE_FILE = Path(
    "data/market_cache.json"
)

# From the comments in Scraper-main/main.py
DEFAULT_COMPETITORS = [

    730,

    892970,

    1943950,

    2767030,

    4223440
]


class SteamMarket:

    def __init__(self):

        self.session = requests.Session()

        if CACHE_FILE.exists():

            with open(

                CACHE_FILE,

                "r",

                encoding="utf-8"

            ) as f:

                self.cache = json.load(f)

        else:

            self.cache = {}

    def get_json(

        self,

        url,

        params=None
    ):

        response = self.session.get(

            url,

            params=params,

            timeout=30
        )

        response.raise_for_status()

        return response.json()

    def app_details(

        self,

        app_id
    ):

        data = self.get_json(

            "https://store.steampowered.com/api/appdetails",

            {"appids": app_id, "cc": "us", "l": "english"}
        )

        entry = data.get(str(app_id), {})

        if not entry.get("success"):

            return {}

        info = entry["data"]

        price = info.get(
            "price_overview",
            {}
        )

        return {

            "name":
            info.get("name"),

            "genres":
            [g["description"] for g in info.get("genres", [])],

            "is_free":
            info.get("is_free", False),

            "price_usd":
            price.get("final", 0) / 100,

            "release_date":
            info.get("release_date", {}).get("date"),

            "developers":
            info.get("developers", [])
        }

    def review_summary(

        self,

        app_id
    ):

        data = self.get_json(

            f"https://store.steampowered.com/appreviews/{app_id}",

            {

                "json": 1,

                "num_per_page": 0,

                "language": "all",

                "purchase_type": "all"
            }
        )

        summary = data.get(
            "query_summary",
            {}
        )

        return {

            "total_positive":
            summary.get("total_positive", 0),

            "total_negative":
            summary.get("total_negative", 0),

            "total_reviews":
            summary.get("total_reviews", 0),

            "review_score_desc":
            summary.get("review_score_desc", "")
        }

    def steamspy(

        self,

        app_id
    ):

        data = self.get_json(

            "https://steamspy.com/api.php",

            {"request": "appdetails", "appid": app_id}
        )

        return {

            "owners":
            data.get("owners", ""),

            "ccu":
            data.get("ccu", 0),

            "average_playtime_hours":
            round(data.get("average_forever", 0) / 60, 1)
        }

    def snapshot(

        self,

        app_id
    ):

        # Live fetch with a cached fallback so the
        # dashboard still renders offline.

        key = str(app_id)

        try:

            details = self.app_details(app_id)

            reviews = self.review_summary(app_id)

            try:

                spy = self.steamspy(app_id)

            except (requests.RequestException, ValueError):

                spy = {}

            snap = {

                "app_id":
                int(app_id),

                **details,

                **reviews,

                **spy,

                "fetched_at":
                datetime.now().isoformat()
            }

            snap.update(
                estimate_sales(snap)
            )

            self.cache[key] = snap

        except (requests.RequestException, ValueError) as e:

            print(
                f"Steam fetch failed for {app_id}: {e}"
            )

            snap = self.cache.get(key, {

                "app_id": int(app_id),

                "error": str(e)
            })

        return snap

    def save_cache(self):

        CACHE_FILE.parent.mkdir(
            exist_ok=True
        )

        with open(

            CACHE_FILE,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                self.cache,

                f,

                ensure_ascii=False,

                indent=4
            )

    def build_report(

        self,

        app_id,

        competitor_ids=None
    ):

        competitor_ids = [

            c

            for c in (competitor_ids or DEFAULT_COMPETITORS)

            if int(c) != int(app_id)
        ]

        report = {

            "game":
            self.snapshot(app_id),

            "competitors":
            [self.snapshot(c) for c in competitor_ids],

            "generated_at":
            datetime.now().isoformat()
        }

        self.save_cache()

        return report


def parse_owners(owners):

    numbers = [

        int(n.replace(",", ""))

        for n in re.findall(r"[\d,]+", str(owners))

        if n.replace(",", "")
    ]

    if len(numbers) >= 2:

        return numbers[0], numbers[1]

    return 0, 0


def estimate_sales(snap):

    # Steam publishes no sales data. Owners come from
    # SteamSpy's range; revenue = midpoint x current price.

    low, high = parse_owners(
        snap.get("owners", "")
    )

    owners_mid = (low + high) // 2

    price = snap.get(
        "price_usd",
        0
    ) or 0

    return {

        "owners_low":
        low,

        "owners_high":
        high,

        "owners_estimate":
        owners_mid,

        "revenue_estimate_usd":
        round(owners_mid * price, 2),

        "positive_ratio":
        round(

            snap.get("total_positive", 0)

            /

            max(snap.get("total_reviews", 0), 1)

            * 100,

            1
        )
    }
