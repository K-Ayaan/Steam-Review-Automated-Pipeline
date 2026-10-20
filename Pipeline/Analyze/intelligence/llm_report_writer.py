import os
import requests


class LLMReportWriter:

    def __init__(self):

        self.url = (
            "http://localhost:11434/api/generate"
        )

        self.model = (
            os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
        )

    def generate(

        self,

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

                f"- {issue['issue_id']} | "

                f"Mentions: {issue['count']} | "

                f"Impact: {issue['impact_score']} | "

                f"Helpful Votes: {issue['helpful_count']}\n"

            )

        prompt = f"""
You are a Senior Game Product Manager.

Analyze the game intelligence report.

Health Score Interpretation:

0-30 = Critical
31-50 = Poor
51-70 = Average
71-85 = Good
86-100 = Excellent

If Overall Health is below 50,
describe the game as being in poor condition.

If Review Health is below 40,
state that player sentiment is strongly negative.

Overall Health:
{health_scores['overall_health']}

Technical Health:
{health_scores.get('technical_health', 100)}

Gameplay Health:
{health_scores.get('gameplay_health', 100)}

Review Health:
{health_scores.get('review_health', 100)}

Issue Health:
{health_scores.get('issue_health', 100)}

Top Issues:
{issue_text}

Write a concise report with:

1. Executive Summary

2. Top Problems

3. Recommended Actions

4. Business Risk

Maximum 250 words.

Return plain text only.
"""

        response = requests.post(

            self.url,

            json={

                "model":
                self.model,

                "prompt":
                prompt,

                "stream":
                False,

                "options": {

                    "temperature": 0.2,

                    "num_predict": 400

                }
            }
        )

        result = response.json()

        return result["response"]