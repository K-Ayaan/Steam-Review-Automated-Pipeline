class ExecutiveSummaryGenerator:

    def generate(
        self,
        report,
        health_scores
    ):

        lines = []

        lines.append(
            "GAME HEALTH SUMMARY"
        )

        lines.append(
            "=" * 60
        )

        lines.append("")

        lines.append(
            f"Overall Health: "
            f"{health_scores['overall_health']}/100"
        )

        lines.append("")

        lines.append(
            "TOP RISKS"
        )

        lines.append("")

        for i, issue in enumerate(
            report[:5],
            start=1
        ):

            lines.append(
                f"{i}. {issue['issue_id']}"
            )

            lines.append(
                f"   Severity: {issue['severity']}"
            )

            lines.append(
                f"   Business Impact: "
                f"{issue['business_impact']}"
            )

            lines.append(
                f"   Team: {issue['team']}"
            )

            lines.append("")
            
        lines.append(
            "RECOMMENDED FOCUS"
        )

        lines.append("")

        for issue in report[:3]:

            lines.append(
                f"- {issue['issue_id']}"
            )

        return "\n".join(
            lines
        )