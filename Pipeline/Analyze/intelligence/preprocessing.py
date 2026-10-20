import re
import pandas as pd


class ReviewPreprocessor:

    def __init__(self, input_file):

        self.input_file = input_file

        self.df = pd.read_csv(input_file)

    def extract_hours(self, value):

        if pd.isna(value):
            return 0.0

        match = re.search(
            r"([\d.]+)",
            str(value)
        )

        if match:
            return float(match.group(1))

        return 0.0

    def clean_text(self, text):

        if pd.isna(text):
            return ""

        text = str(text)

        text = text.replace("\n", " ")

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    def create_features(self):

        # Positive / Negative

        self.df["is_positive"] = (
            self.df["recommendation"]
            .astype(str)
            .str.strip()
            .eq("Recommended")
        )

        # Playtime

        self.df["playtime_hours"] = (
            self.df["hours_played"]
            .apply(self.extract_hours)
        )

        # Review Length

        self.df["review_length"] = (
            self.df["review_text"]
            .astype(str)
            .str.len()
        )

        # Engagement

        self.df["engagement_score"] = (
            self.df["helpful_count"]
            +
            self.df["funny_count"]
        )

        # Clean Text

        self.df["clean_review_text"] = (
            self.df["review_text"]
            .apply(self.clean_text)
        )

        return self.df

    def save(self, output_file):

        self.df.to_csv(
            output_file,
            index=False,
            encoding="utf-8-sig"
        )

        print(
            f"Saved: {output_file}"
        )