from collections import defaultdict


class IssueDatabase:

    def __init__(self):

        self.issues = defaultdict(

            lambda: {

                "count": 0,

                "impact_score": 0,

                "helpful_count": 0,

                "languages": defaultdict(int),

                "player_segments": defaultdict(int),

                "positive_count": 0,

                "negative_count": 0,

                "reviews": []
            }
        )

    def add_review(
        self,
        issues,
        review_text,
        language,
        player_segment,
        impact_score,
        helpful_count
    ):

        for issue in issues:

            issue_id = issue["issue_id"]

            sentiment = issue.get(

                "sentiment",

                "unknown"
            )

            self.issues[
                issue_id
            ]["count"] += 1

            if sentiment == "positive":

                self.issues[
                    issue_id
                ][
                    "positive_count"
                ] += 1

            elif sentiment == "negative":

                self.issues[
                    issue_id
                ][
                    "negative_count"
                ] += 1



            self.issues[
                issue_id
            ]["impact_score"] += (
                impact_score
            )

            self.issues[
                issue_id
            ]["helpful_count"] += (
                helpful_count
            )

            self.issues[
                issue_id
            ]["languages"][
                language
            ] += 1

            self.issues[
                issue_id
            ]["player_segments"][
                player_segment
            ] += 1


            priority_score = (

                impact_score

                +

                helpful_count

                +

                min(

                    len(review_text) / 200,

                    10

                )
            )

            self.issues[issue_id]["reviews"].append({

                "review_text":
                review_text,

                "language":
                language,

                "impact_score":
                impact_score,

                "helpful_count":
                helpful_count,

                "issue_id":
                issue_id,

                "priority_score":

                    impact_score

                    +

                    helpful_count
            })

    def summary(self):

        return self.issues
    
    def get_top_reviews(

        self,

        issue_id,

        limit=3

    ):

        reviews = (

            self.issues[issue_id]

            ["reviews"]
        )

        reviews = sorted(

            reviews,

            key=lambda x:

            x["priority_score"],

            reverse=True
        )

        selected = []

        seen = set()

        for review in reviews:

            text = review["review_text"][:150]

            if text in seen:
                continue

            seen.add(text)

            selected.append(review)

            if len(selected) >= limit:
                break

        return selected