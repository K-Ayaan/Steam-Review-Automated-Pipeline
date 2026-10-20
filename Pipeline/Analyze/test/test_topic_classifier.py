from intelligence.topic_classifier import (
    TopicClassifier
)

classifier = TopicClassifier(
    "data/engineered_reviews.csv"
)

df = classifier.classify()

print(
    df[
        [
            "topics",
            "clean_review_text"
        ]
    ].head(10)
)

classifier.save(
    "data/topic_reviews.csv"
)

print(
    "\nTopic Classification Complete"
)


print(df["topics"].value_counts())