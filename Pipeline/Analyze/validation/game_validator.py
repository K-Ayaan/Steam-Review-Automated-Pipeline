import pandas as pd


class GameValidator:

    def validate(
        self,
        df,
        issue_column="issues"
    ):

        total_reviews = len(df)

        no_issue = 0

        for issues in df[issue_column]:

            if "NO_ISSUE" in str(issues):

                no_issue += 1

        coverage = round(

            (
                total_reviews
                -
                no_issue
            )

            /

            total_reviews

            * 100,

            2
        )

        return {

            "total_reviews":
            total_reviews,

            "no_issue_reviews":
            no_issue,

            "coverage":
            coverage
        }