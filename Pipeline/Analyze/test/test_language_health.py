import pandas as pd

df = pd.read_csv(
    "data/language_reviews.csv"
)

summary = (
    df.groupby("language")
      ["is_positive"]
      .agg(
          total_reviews="count",
          positive_reviews="sum"
      )
)

summary["negative_reviews"] = (
    summary["total_reviews"]
    -
    summary["positive_reviews"]
)

summary["positive_rate"] = (
    summary["positive_reviews"]
    /
    summary["total_reviews"]
    * 100
).round(2)

summary = summary.sort_values(
    "total_reviews",
    ascending=False
)

print(summary.head(15))