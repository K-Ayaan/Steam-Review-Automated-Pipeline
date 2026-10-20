import pandas as pd

from intelligence.preprocessing import (
    ReviewPreprocessor
)

from intelligence.feature_engineering import (
    FeatureEngineer
)

from intelligence.language_detector import (
    LanguageDetector
)


INPUT_FILE = "data/reviews.csv"

GAME_NAME = "The Cursed Hour"

TEMP_FILE = "data/preprocessed_reviews.csv"

OUTPUT_FILE = "data/language_reviews.csv"


def generate_dataset(

    game_name=GAME_NAME,

    input_file=INPUT_FILE,

    output_file=OUTPUT_FILE
):

    # STEP 1
    # Basic preprocessing

    df_raw = pd.read_csv(
        input_file
    )

    if "review_id" not in df_raw.columns:

        df_raw.insert(
            0,
            "review_id",
            range(
                1,
                len(df_raw) + 1
            )
        )

    if "game_name" not in df_raw.columns:

        df_raw["game_name"] = (
            game_name
        )

    df_raw.to_csv(

        input_file,

        index=False,

        encoding="utf-8-sig"
    )

    processor = ReviewPreprocessor(
        input_file
    )

    processor.create_features()

    processor.save(
        TEMP_FILE
    )

    print(
        "Preprocessing Complete"
    )

    # STEP 2
    # Feature Engineering

    engineer = FeatureEngineer(
        TEMP_FILE
    )

    df = engineer.create_features()

    print(
        "Feature Engineering Complete"
    )

    # STEP 3
    # Language Detection

    detector = LanguageDetector()

    df["language"] = (

        df["review_text"]

        .apply(
            detector.detect_language
        )
    )

    print(
        "Language Detection Complete"
    )

    # STEP 4
    # Save Final Dataset

    df.to_csv(

        output_file,

        index=False,

        encoding="utf-8-sig"
    )

    print(
        f"Saved: {output_file}"
    )

    print(
        f"Rows: {len(df)}"
    )

    print(
        df.columns.tolist()
    )

    return df


if __name__ == "__main__":

    generate_dataset()
