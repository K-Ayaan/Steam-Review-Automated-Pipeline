from intelligence.feature_engineering import (
    FeatureEngineer
)

engineer = FeatureEngineer(
    "data/enriched_reviews.csv"
)

df = engineer.create_features()

print(
    df[
        [
            "playtime_hours",
            "player_segment",
            "engagement_tier",
            "impact_score"
        ]
    ].head()
)

engineer.save(
    "data/engineered_reviews.csv"
)

print(
    "Feature Engineering Complete"
)

print(df["player_segment"].value_counts())