from intelligence.issue_miner import (
    IssueMiner
)

miner = IssueMiner(
    "data/language_reviews.csv"
)

top_issues = (
    miner.highest_impact_negative(20)
)

print(
    top_issues[
        [
            "impact_score",
            "language",
            "review_text"
        ]
    ]
)