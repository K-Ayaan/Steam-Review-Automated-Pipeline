import pandas as pd

from sentence_transformers import (
    SentenceTransformer
)

import umap

import hdbscan


class ReviewClustering:

    def __init__(self, input_file):

        self.df = pd.read_csv(input_file)

        self.model = SentenceTransformer(
            "paraphrase-multilingual-MiniLM-L12-v2"
        )

    def generate_embeddings(self):

        reviews = (
            self.df[
                "clean_review_text"
            ]
            .fillna("")
            .tolist()
        )

        embeddings = (
            self.model.encode(
                reviews,
                show_progress_bar=True
            )
        )

        return embeddings

    def cluster_reviews(
        self,
        embeddings
    ):

        reducer = umap.UMAP(
            n_neighbors=15,
            n_components=10,
            metric="cosine"
        )

        reduced = reducer.fit_transform(
            embeddings
        )

        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=10,
            metric="euclidean"
        )

        labels = clusterer.fit_predict(
            reduced
        )

        self.df["cluster"] = labels

        return self.df