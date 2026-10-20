import pandas as pd

df = pd.read_csv(
    "data/clustered_reviews.csv"
)

for cluster_id in sorted(
    df["cluster"].unique()
):

    print(
        f"\n\n===== CLUSTER {cluster_id} ====="
    )

    sample = (
        df[
            df["cluster"]
            == cluster_id
        ]
        [
            [
                "language",
                "review_text"
            ]
        ]
        .head(5)
    )

    print(sample)