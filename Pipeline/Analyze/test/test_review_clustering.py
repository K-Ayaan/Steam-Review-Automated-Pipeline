from intelligence.review_clustering import (
    ReviewClustering
)

clusterer = ReviewClustering(
    "data/language_reviews.csv"
)

embeddings = (
    clusterer.generate_embeddings()
)

df = clusterer.cluster_reviews(
    embeddings
)

print(
    df["cluster"]
    .value_counts()
)

df.to_csv(
    "data/clustered_reviews.csv",
    index=False
)

print(
    "Clustering Complete"
)