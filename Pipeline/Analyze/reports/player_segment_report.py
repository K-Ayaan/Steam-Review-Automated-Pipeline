from collections import defaultdict


class PlayerSegmentReport:

    def generate(

        self,

        issue_database

    ):

        segment_issues = (

            defaultdict(list)
        )

        for issue_id, data in (

            issue_database.items()

        ):

            if issue_id == "NO_ISSUE":

                continue

            top_segment = max(

                data["player_segments"],

                key=data[
                    "player_segments"
                ].get
            )

            segment_issues[
                top_segment
            ].append({

                "issue_id":
                issue_id,

                "count":
                data["count"],

                "impact_score":
                data[
                    "impact_score"
                ]
            })

        lines = []

        lines.append(
            "PLAYER SEGMENT REPORT"
        )

        lines.append(
            "=" * 60
        )

        for segment, issues in (

            segment_issues.items()

        ):

            issues = sorted(

                issues,

                key=lambda x: (

                    x["impact_score"],

                    x["count"]
                ),

                reverse=True
            )

            lines.append("")

            lines.append(
                segment
            )

            lines.append(
                "-" * 30
            )

            lines.append(
                "Top Issues:"
            )

            for issue in issues[:5]:

                lines.append(

                    f"- {issue['issue_id']} "

                    f"(Mentions: {issue['count']})"
                )

        return "\n".join(
            lines
        )
