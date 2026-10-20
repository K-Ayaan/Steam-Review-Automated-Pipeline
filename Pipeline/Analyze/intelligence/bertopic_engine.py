import pandas as pd

from bertopic import BERTopic

from sentence_transformers import (
    SentenceTransformer
)


class GameTopicEngine:

    def __init__(self, input_file):

        self.df = pd.read_csv(input_file)

        self.model = SentenceTransformer(
            "paraphrase-multilingual-MiniLM-L12-v2"
        )

    def build_topics(self):

        documents = (
            self.df["clean_review_text"]
            .fillna("")
            .tolist()
        )

        topic_model = BERTopic(
            embedding_model=self.model,
            language="multilingual",
            calculate_probabilities=False,
            verbose=True
        )

        topics, probs = (
            topic_model.fit_transform(
                documents
            )
        )

        self.df["topic_id"] = topics

        return topic_model, self.df