def build_report_prompt(

    report,

    health_scores

):

    top_issues = sorted(

        report,

        key=lambda x: x["count"],

        reverse=True

    )[:5]

    issue_text = ""

    for issue in top_issues:

        issue_text += (

            f"- {issue['issue_id']} "

            f"({issue['count']} mentions)\n"

        )

    return f"""
You are a Senior Game Product Manager.

Analyze the following game intelligence report.

Overall Health:
{health_scores['overall_health']}

Technical Health:
{health_scores.get('technical_health', 100)}

Gameplay Health:
{health_scores.get('gameplay_health', 100)}

Top Issues:

{issue_text}

Write:

1. Executive Summary

2. Top Problems

3. Recommended Actions

4. Business Risk

Maximum 250 words.

Return plain text only.
"""