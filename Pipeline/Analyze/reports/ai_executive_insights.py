import os
import requests


class AIExecutiveInsights:

    def generate(

        self,

        executive_summary,

        impact_report,

        audience_report,

        campaign_report
    ):

        prompt = f"""

You are a senior gaming industry consultant.

Generate:

1. Key Findings
2. Business Risks
3. Recommended Actions
4. Marketing Recommendations

Executive Summary:
{executive_summary}

Update Impact:
{impact_report}

Audience:
{audience_report}

Campaign:
{campaign_report}

Keep response under 500 words.
"""

        response = requests.post(

            "http://localhost:11434/api/generate",

            json={

                "model":
                os.getenv("OLLAMA_MODEL", "qwen2.5:7b"),

                "prompt":
                prompt,

                "stream":
                False
            }
        )

        return response.json()[

            "response"
        ]