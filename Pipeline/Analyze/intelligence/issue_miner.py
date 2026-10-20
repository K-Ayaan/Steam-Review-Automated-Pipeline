import pandas as pd


class IssueMiner:

    def __init__(self, input_file):

        self.df = pd.read_csv(input_file)

    def negative_reviews(self):

        return self.df.loc[~self.df["is_positive"]]

    def highest_impact_negative(
        self,
        top_n=20
    ):

        negatives = (
            self.negative_reviews()
            .sort_values(
                "impact_score",
                ascending=False
            )
        )

        return negatives.head(top_n)