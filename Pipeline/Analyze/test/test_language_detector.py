from intelligence.language_detector import (
    LanguageDetector
)

detector = LanguageDetector(
    "data/engineered_reviews.csv"
)

df = detector.process()

print(
    df["language"]
    .value_counts()
)

detector.save(
    "data/language_reviews.csv"
)