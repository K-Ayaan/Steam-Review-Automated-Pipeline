from reportlab.platypus import (
SimpleDocTemplate,
Paragraph,
Spacer,
PageBreak,
Table,
TableStyle
)

from reportlab.lib import colors

from reportlab.lib.styles import (
getSampleStyleSheet
)

class PDFExporter:

    def export(

        self,

        output_path,

        metadata,

        health_scores,

        issues,

        audience_report,

        campaign_report,

        executive_summary,

        ai_insights,

        segment_campaigns

    ):

        doc = SimpleDocTemplate(
            str(output_path)
        )

        styles = (
            getSampleStyleSheet()
        )

        story = []

        # COVER PAGE

        story.append(

            Paragraph(

                f"{metadata['game_name']}",

                styles["Title"]
            )
        )

        story.append(

            Paragraph(

                "Game Intelligence Report",

                styles["Heading2"]
            )
        )

        story.append(
            Spacer(1, 20)
        )

        story.append(

            Paragraph(

                f"Version: {metadata.get('game_version','Unknown')}",

                styles["BodyText"]
            )
        )

        story.append(

            Paragraph(

                f"Reviews Analysed: {metadata['review_count']}",

                styles["BodyText"]
            )
        )

        story.append(

            Paragraph(

                f"Review Window: {metadata.get('review_start_date','')} → {metadata.get('review_end_date','')}",

                styles["BodyText"]
            )
        )

        story.append(
            Spacer(1, 20)
        )

        summary_text = f"""
        Overall Health: {health_scores['overall_health']}<br/>
        Review Health: {health_scores['review_health']}<br/>
        Issue Health: {health_scores['issue_health']}
        """

        story.append(

            Paragraph(

                summary_text,

                styles["BodyText"]
            )
        )

        story.append(
            PageBreak()
        )

        # HEALTH OVERVIEW

        story.append(

            Paragraph(

                "Health Overview",

                styles["Heading1"]
            )
        )

        health_table = [

            ["Metric", "Score"],

            ["Overall Health",
            health_scores["overall_health"]],

            ["Review Health",
            health_scores["review_health"]],

            ["Issue Health",
            health_scores["issue_health"]],

            ["Gameplay Health",
            health_scores["gameplay_health"]],

            ["Technical Health",
            health_scores["technical_health"]]
        ]

        table = Table(
            health_table
        )

        table.setStyle(

            TableStyle([

                ("GRID",(0,0),(-1,-1),1,
                colors.black),

                ("BACKGROUND",
                (0,0),(-1,0),
                colors.lightgrey)
            ])
        )

        story.append(table)

        story.append(
            Spacer(1,20)
        )

        # TOP ISSUES

        story.append(

            Paragraph(

                "Top Issues",

                styles["Heading1"]
            )
        )

        issue_table = [

            [

                "Issue",

                "Severity",

                "Count",

                "Impact"
            ]
        ]

        for issue in issues[:10]:

            issue_table.append([

                issue["issue_id"],

                issue["severity"],

                str(issue["count"]),

                str(issue["impact_score"])
            ])

        table = Table(
            issue_table
        )

        table.setStyle(

            TableStyle([

                ("GRID",(0,0),(-1,-1),1,
                colors.black),

                ("BACKGROUND",
                (0,0),(-1,0),
                colors.lightgrey)
            ])
        )

        story.append(table)

        story.append(
            PageBreak()
        )

        # AUDIENCE

        story.append(

            Paragraph(

                "Audience Intelligence",

                styles["Heading1"]
            )
        )

        audience_text = "<br/>".join(

            audience_report[
                "target_audiences"
            ]
        )

        story.append(

            Paragraph(

                audience_text,

                styles["BodyText"]
            )
        )

        story.append(
            Spacer(1,20)
        )

        story.append(

            Paragraph(

                "Marketing Strategy",

                styles["Heading1"]
            )
        )

        promote = "<br/>".join(

            campaign_report.get(
                "promote",
                []
            )
        )

        avoid = "<br/>".join(

            campaign_report.get(
                "avoid",
                []
            )
        )

        story.append(

            Paragraph(

                f"<b>Promote</b><br/>{promote}",

                styles["BodyText"]
            )
        )

        story.append(
            Spacer(1,10)
        )

        story.append(

            Paragraph(

                f"<b>Avoid</b><br/>{avoid}",

                styles["BodyText"]
            )
        )

        story.append(
            PageBreak()
        )

        # AI INSIGHTS

        story.append(

            Paragraph(

                "AI Strategic Recommendations",

                styles["Heading1"]
            )
        )

        ai_lines = (

            str(ai_insights)

            .replace("###", "")

            .replace("**", "")

            .split("\n")
        )

        for line in ai_lines:

            line = line.strip()

            if not line:

                story.append(
                    Spacer(1, 6)
                )

                continue

            story.append(

                Paragraph(

                    line,

                    styles["BodyText"]
                )
            )

        story.append(
            PageBreak()
        )

        # SEGMENT CAMPAIGNS

        story.append(

            Paragraph(

                "Segment Campaigns",

                styles["Heading1"]
            )
        )

        for campaign in segment_campaigns:

            story.append(

                Paragraph(

                    campaign["audience"],

                    styles["Heading2"]
                )
            )

            story.append(

                Paragraph(

                    campaign.get(
                        "ad_copy",
                        ""
                    ),

                    styles["BodyText"]
                )
            )

            story.append(
                Spacer(1,10)
            )

        doc.build(story)

