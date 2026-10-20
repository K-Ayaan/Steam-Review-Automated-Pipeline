import pandas as pd

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)


class OntologyExpander:

    def __init__(self, input_file):

        self.df = pd.read_csv(input_file)

    def unknown_reviews(self):

        return self.df[
            self.df["issues"] == "UNKNOWN"
        ]

    def discover_terms(
        self,
        top_n=100
    ):

        unknown_df = self.unknown_reviews()

        texts = (
            unknown_df[
                "clean_review_text"
            ]
            .fillna("")
            .tolist()
        )

        if len(texts) == 0:

            return pd.DataFrame()

        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=500
        )

        matrix = vectorizer.fit_transform(
            texts
        )

        terms = (
            vectorizer
            .get_feature_names_out()
        )

        scores = (
            matrix.sum(axis=0)
            .A1
        )

        results = pd.DataFrame({

            "term": terms,

            "score": scores

        })

        results = (
            results
            .sort_values(
                "score",
                ascending=False
            )
            .head(top_n)
        )

        return results