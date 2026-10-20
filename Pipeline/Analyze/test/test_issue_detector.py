from intelligence.issue_detector import (
    IssueDetector
)

detector = IssueDetector(
    "data/engineered_reviews.csv"
)

print(
    "\nPLAYER SEGMENT HEALTH\n"
)

print(
    detector.review_health()
)

print(
    "\nTOP NEGATIVE REVIEWS\n"
)

top_reviews = (
    detector.top_negative_reviews(5)
)

print(
    top_reviews[
        [
            "player_segment",
            "impact_score",
            "review_text"
        ]
    ]
)
