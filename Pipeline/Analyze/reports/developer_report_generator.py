from intelligence.developer_agent import (
    DeveloperAgent
)

from intelligence.sprint_planner import (
    SprintPlanner
)


class DeveloperReportGenerator:

    def __init__(self):

        self.agent = (
            DeveloperAgent()
        )

        self.sprint_planner = (
            SprintPlanner()
        )

    def generate(
        self,
        report
    ):

        lines = []

        lines.append(
            "GAME INTELLIGENCE REPORT"
        )

        lines.append(
            "=" * 60
        )

        rank = 1

        for issue in report:

            lines.append("")

            lines.append(
                f"TOP ISSUE #{rank}"
            )

            lines.append(
                f"Issue: {issue['issue_id']}"
            )

            lines.append(
                f"Severity: {issue['severity']}"
            )

            lines.append(
                f"Priority: {issue['priority']}"
            )

            lines.append(
                f"Department: {issue['department']}"
            )

            lines.append(
                f"Team: {issue['team']}"
            )

            lines.append(
                f"Category: {issue['category']}"
            )

            lines.append(
                f"Mentions: {issue['count']}"
            )

            lines.append(
                f"Impact Score: {issue['impact_score']}"
            )

            lines.append(
                f"Helpful Votes: {issue['helpful_count']}"
            )

            lines.append(
                f"Business Impact: {issue['business_impact']}"
            )

            lines.append(
                f"Top Language: {issue['top_language']}"
            )

            lines.append(
                f"Top Player Segment: {issue['top_player_segment']}"
            )

            lines.append("")
            lines.append(
                "Recommended Actions:"
            )

            actions = self.agent.recommend(
                issue["issue_id"]
            )

            plan = (

                self.sprint_planner.plan(
                    issue
                )
            )

            for action in actions:

                lines.append(
                    f" - {action}"
                )

            lines.append("")

            lines.append(
                "Sprint Recommendation"
            )

            lines.append(
                f"Priority: {plan['priority']}"
            )

            lines.append(
                f"Story Points: {plan['story_points']}"
            )

            lines.append(
                f"Expected Impact: {plan['impact']}"
            )

            lines.append("")

            lines.append(
                "Suggested Sprint Tasks:"
            )

            for task in plan["tasks"]:

                lines.append(
                    f" - {task}"
                )

            lines.append("")
            lines.append(
                "Top Evidence Reviews:"
            )

            top_reviews = issue.get(
                "top_reviews",
                []
            )

            for idx, review in enumerate(
                top_reviews,
                start=1
            ):

                lines.append("")

                lines.append(
                    f"[{idx}]"
                )

                lines.append(
                    review["review_text"][:500]
                )

                lines.append(
                    f"Impact Score: {review['impact_score']}"
                )

                lines.append(
                    f"Helpful Votes: {review['helpful_count']}"
                )

            lines.append(
                "-" * 60
            )

            rank += 1

        return "\n".join(
            lines
        )