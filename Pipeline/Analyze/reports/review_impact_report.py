from intelligence.review_impact_predictor import (
    ReviewImpactPredictor
)


class ReviewImpactReport:

    def __init__(self):

        self.predictor = (

            ReviewImpactPredictor()
        )

    def generate(

        self,

        issues
    ):

        report = []

        for issue in issues:

            report.append(

                self.predictor.predict(
                    issue
                )
            )

        return report