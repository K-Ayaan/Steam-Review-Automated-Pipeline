class EvidenceReportGenerator:

    def generate(
        self,
        issue_database,
        top_n=3
    ):

        report = []

        for issue_id, data in (
            issue_database.items()
        ):

            if issue_id == "NO_ISSUE":
                continue

            report.append(
                f"\n{'='*60}"
            )

            report.append(
                f"\nISSUE: {issue_id}\n"
            )

            reviews = sorted(

                data["reviews"],

                key=lambda x: (

                    x["impact_score"],

                    x["helpful_count"]
                ),

                reverse=True
            )

            for i, review in enumerate(
                reviews[:top_n],
                start=1
            ):

                report.append(
                    f"\nEvidence #{i}"
                )

                report.append(
                    f"Impact: {review['impact_score']}"
                )

                report.append(
                    f"Helpful: {review['helpful_count']}"
                )

                report.append(
                    review["review_text"][:500]
                )

                report.append(
                    "\n" + "-"*40
                )

        return "\n".join(report)