import pandas as pd


class ReviewIntelligence:

    def __init__(self, input_file):

        self.df = pd.read_csv(input_file)

    def top_positive(self, n=10):

        return (
            self.df[
                self.df["is_positive"]
            ]
            .sort_values(
                "impact_score",
                ascending=False
            )
            .head(n)
        )

    def top_negative(self, n=10):

        return (
            self.df[
                ~self.df["is_positive"]
            ]
            .sort_values(
                "impact_score",
                ascending=False
            )
            .head(n)
        )