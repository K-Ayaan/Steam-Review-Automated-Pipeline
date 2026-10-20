import pandas as pd
import json

def save_reviews(reviews, path):

    df = pd.DataFrame(reviews)

    df.to_csv(
        path,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"Saved {len(df)} reviews"
    )

def save_checkpoint(
    page,
    params
):

    checkpoint = {
        "page": page,
        "params": params
    }

    with open(
        "data/checkpoint.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            checkpoint,
            f,
            ensure_ascii=False,
            indent=4
        )

def load_checkpoint():

    try:

        with open(
            "data/checkpoint.json",
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return {}