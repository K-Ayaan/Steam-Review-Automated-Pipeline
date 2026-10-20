# import math


# class SeverityEngine:

#     PRIOR_ISSUES = 5
#     PRIOR_REVIEWS = 100

#     def calculate(
#         self,
#         issue_id,
#         issue_data,
#         known_reviews
#     ):
#         if issue_id == "NO_ISSUE":
#             return "IGNORE"

#         issue_count = issue_data["count"]
#         impact_score = issue_data.get("impact_score", 0)
#         helpful_count = issue_data.get("helpful_count", 0)

#         # Bayesian-smoothed issue rate
#         adjusted_rate = (
#             issue_count + self.PRIOR_ISSUES
#         ) / (
#             known_reviews + self.PRIOR_REVIEWS
#         )

#         # Composite severity score
#         score = (
#             adjusted_rate * 100
#             + impact_score * 0.5
#             + math.log1p(helpful_count) * 2
#         )

#         if score >= 30:
#             return "CRITICAL"
#         elif score >= 20:
#             return "HIGH"
#         elif score >= 10:
#             return "MEDIUM"
#         else:
#             return "LOW"
        
import math


class SeverityEngine:

    def calculate(
        self,
        issue_id,
        issue_data,
        known_reviews
    ):

        if issue_id == "NO_ISSUE":
            return {
                "severity": "IGNORE",
                "score": 0
            }

        count = issue_data["count"]
        impact_score = issue_data["impact_score"]
        helpful_count = issue_data["helpful_count"]


        # Bayesian smoothing
        issue_penetration = (

            count

            /

            max(
                known_reviews,
                1
            )
        )

        score = (

            issue_penetration

            * 100

            * impact_score

            +

            math.log1p(
                helpful_count
            )
        )

        return {
            "severity": "PENDING",
            "score": round(score, 2)

        }