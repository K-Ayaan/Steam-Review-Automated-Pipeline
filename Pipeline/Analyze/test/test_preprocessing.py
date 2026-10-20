from intelligence.preprocessing import (
    ReviewPreprocessor
)


processor = ReviewPreprocessor(
    "data/reviews.csv"
)

df = processor.create_features()

print(
    df[
        [
            "recommendation",
            "playtime_hours",
            "review_length",
            "engagement_score"
        ]
    ].head()
)

processor.save(
    "data/enriched_reviews.csv"
)