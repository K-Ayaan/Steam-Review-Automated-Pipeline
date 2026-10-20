from intelligence.bertopic_engine import (
    GameTopicEngine
)

engine = GameTopicEngine(
    "data/language_reviews.csv"
)

topic_model, df = (
    engine.build_topics()
)

print("---------------------",
    topic_model.get_topic_info()
)

df.to_csv(
    "data/topic_modeled_reviews.csv",
    index=False
)