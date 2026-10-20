from intelligence.review_intelligence import (
    ReviewIntelligence
)

intel = ReviewIntelligence(
    "data/engineered_reviews.csv"
)

print(
    intel.top_negative(10)[
        [
            "impact_score",
            "helpful_count",
            "review_text"
        ]
    ]
)