import os
import requests

class AdGenerator:

    def __init__(self):

        self.url = "http://localhost:11434/api/generate"

        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

    def generate(

        self,

        game_name,

        marketing_report,

        marketing_confidence,

        health_scores,

        genre_profile

    ):
        
        confidence = marketing_confidence[
            "marketing_confidence"
        ]

        recommendation = marketing_confidence[
            "recommendation"
        ]

        high_risk_issues = marketing_report.get(
            "high_risk_issues",
            []
        )

        overall_health = health_scores[
            "overall_health"
        ]

        if confidence >= 80:

            marketing_mode = (
                "Aggressive Growth"
            )

        elif confidence >= 60:

            marketing_mode = (
                "Balanced Growth"
            )

        else:

            marketing_mode = (
                "Retention & Community"
            )

        prompt = f"""
You are a senior game marketing manager.

Game:
{game_name}

Game Genre:
{genre_profile['genre']}

Core Game Pillars:
{genre_profile['pillars']}

Top Strengths:
{marketing_report.get('promote', [])}

Major Problems:
{marketing_report.get('avoid', [])}

Target Audience:
{marketing_report.get('target_audiences', [])}

Promote:
{marketing_report.get('promote', [])}

Channels:
{marketing_report.get('recommended_channels', [])}

Issues To Avoid Mentioning:
{high_risk_issues}

Never mention these topics directly.
Do not imply these issues are solved.
Do not use marketing claims related to these areas.

Overall Health:
{overall_health}

Marketing Confidence:
{confidence}

Recommendation:
{recommendation}

Marketing Mode:
{marketing_mode}

Rules:

1. Never promote anything related to High Risk Issues.

2. Never mention issues listed in High Risk Issues.

3. Never imply these issues are fixed.

4. Marketing Modes:

Aggressive Growth
- Focus on excitement
- Focus on acquisition
- Strong CTA
- Competitive messaging
- FOMO is allowed

Balanced Growth
- Focus on strengths
- Moderate CTA
- Highlight core gameplay
- Avoid exaggeration

Retention & Community
- Focus on existing players
- Focus on community
- Focus on updates
- Focus on player feedback
- Avoid overpromising

5. Write ads matching the selected Marketing Mode.

Create:

1. Steam Community Post
2. Discord Announcement
3. Reddit Post

5. Never market outside the game's genre.

6. Only market features aligned with the Core Game Pillars.

7. Competitive FPS games should focus on:
- Skill
- Teamplay
- Ranking
- Competition

8. Horror games should focus on:
- Fear
- Atmosphere
- Suspense

9. Survival games should focus on:
- Exploration
- Building
- Progression

Keep each under 100 words.

Return plain text.
"""

        response = requests.post(

            self.url,

            json={

                "model":
                self.model,

                "prompt":
                prompt,

                "stream":
                False
            }
        )

        data = response.json()

        return data.get(
            "response",
            ""
        )
    

    def generate_segment_ad(

        self,

        campaign,

        marketing_report,

        genre_profile
    ):
        prompt = f"""
        Create a marketing ad.

        Genre:
        {genre_profile['genre']}

        Core Game Pillars:
        {genre_profile['pillars']}

        Audience:
        {campaign['audience']}

        Channel:
        {campaign['channel']}

        Promote:
        {marketing_report.get('promote', [])}

        Avoid:
        {marketing_report.get('avoid', [])}

        Rules:

1. Never market outside the game's genre.

2. Never mention features outside the Core Game Pillars.

3. Focus specifically on the target audience.

4. Keep the tone matching the genre.

5. Keep under 80 words.

Write a short marketing ad.
        """
        response = requests.post(

            self.url,

            json={

                "model":
                self.model,

                "prompt":
                prompt,

                "stream":
                False
            }
        )

        return response.json()["response"]
    

    def generate_creatives(

        self,

        context
    ):

        prompt = f"""
You are a AAA game marketing copywriter.

Game:
{context['game_name']}

Genre:
{context['genre']}

Audience:
{context['audience']}

Platform:
{context['platform']}

Core Pillars:
{context['pillars']}

Promote:
{context['promote']}

Avoid:
{context['avoid']}

Platform Rules:

Reddit:
- Community discussion
- Conversational
- Under 120 words

Discord:
- Short announcement
- Exciting
- Under 80 words

Email:
- Professional
- Marketing focused
- CTA driven
- Structure format:
  1. Subject Line: Under 60 characters with Brand/Platform x Game and Key Metric.
  2. The Hook: High-context reference to target industry/demographic.
  3. The Value: Data-driven bridge using Audience and Pillars data.
  4. The Creative Concept: Specific native ad format (e.g. skin, billboard, reward) tied to playstyle.
  5. The Proof & CTA: Low-friction "yes/no" question to view a 1-page visual mockup.

Rules:

1. Never invent game features.

2. Never invent a game name.

3. Use only the provided pillars.

4. Never mention avoided topics.

Return EXACTLY:

HEADLINE:
<headline>

AD_COPY:
<ad copy>

CTA:
<cta>

Do not use markdown.
Do not use JSON.
Do not add explanations.
"""

        response = requests.post(

            self.url,

            json={

                "model":
                self.model,

                "prompt":
                prompt,

                "stream":
                False
            }
        )

        raw = response.json().get(
            "response",
            ""
        )

        try:

            headline = raw.split(
                "HEADLINE:"
            )[1].split(
                "AD_COPY:"
            )[0].strip()

            ad_copy = raw.split(
                "AD_COPY:"
            )[1].split(
                "CTA:"
            )[0].strip()

            cta = raw.split(
                "CTA:"
            )[1].strip()

            return {

                "headline":
                headline,

                "ad_copy":
                ad_copy,

                "cta":
                cta
            }

        except Exception:

            print(
                "CREATIVE PARSE FAILED"
            )

            print(raw)

            return {

                "headline":
                "Creative Parse Failed",

                "ad_copy":
                raw,

                "cta":
                "Play Now"
            }