import pandas as pd


class IssueDetector:

    def __init__(self, input_file):

        self.df = pd.read_csv(input_file)

    def review_health(self):

        summary = (
            self.df
            .groupby("player_segment")
            ["is_positive"]
            .agg(
                total_reviews="count",
                positive_reviews="sum"
            )
        )

        summary["negative_reviews"] = (
            summary["total_reviews"]
            -
            summary["positive_reviews"]
        )

        summary["positive_rate"] = (
            summary["positive_reviews"]
            /
            summary["total_reviews"]
            * 100
        ).round(2)

        summary["negative_rate"] = (
            summary["negative_reviews"]
            /
            summary["total_reviews"]
            * 100
        ).round(2)

        return summary

    def top_negative_reviews(
        self,
        n=10
    ):

        negative_df = (
            self.df.loc[~self.df["is_positive"]]
            .sort_values(
                "impact_score",
                ascending=False
            )
        )

        return negative_df.head(n)