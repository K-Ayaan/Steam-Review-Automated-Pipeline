import pandas as pd


class IssueExtractor:

    def __init__(self, input_file):

        self.df = pd.read_csv(input_file)

    def candidate_reviews(
        self,
        top_n=100
    ):
        
        negative_reviews = (
            self.df.loc[~self.df["is_positive"]]
            .sort_values("impact_score", ascending=False)
        )


        return negative_reviews.head(top_n)