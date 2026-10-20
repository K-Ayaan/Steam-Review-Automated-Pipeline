import pandas as pd


class FeatureEngineer:

    def __init__(self, input_file):

        self.df = pd.read_csv(input_file)

    def player_segment(self, hours):

        if hours < 2:
            return "New Player"

        elif hours < 20:
            return "Casual Player"

        elif hours < 100:
            return "Core Player"

        else:
            return "Veteran"

    def engagement_tier(self, score):

        if score == 0:
            return "Low"

        elif score < 10:
            return "Medium"

        elif score < 50:
            return "High"

        return "Very High"

    def create_features(self):

        self.df["player_segment"] = (
            self.df["playtime_hours"]
            .apply(self.player_segment)
        )

        self.df["engagement_tier"] = (
            self.df["engagement_score"]
            .apply(self.engagement_tier)
        )

        self.df["impact_score"] = (
            self.df["helpful_count"] * 3
            +
            self.df["funny_count"]
        )

        self.df["review_quality_score"] = (
            self.df["review_length"]
            *
            (
                self.df["engagement_score"] + 1
            )
        )

        return self.df

    def save(self, output_file):

        self.df.to_csv(
            output_file,
            index=False,
            encoding="utf-8-sig"
        )