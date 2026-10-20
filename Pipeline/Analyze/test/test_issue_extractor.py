from intelligence.issue_extractor import (
    IssueExtractor
)

extractor = IssueExtractor(
    "data/language_reviews.csv"
)

issues = (
    extractor.candidate_reviews(50)
)

print(
    issues[
        [
            "impact_score",
            "language",
            "review_text"
        ]
    ]
)