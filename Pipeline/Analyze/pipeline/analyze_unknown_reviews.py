import pandas as pd
import json
from collections import Counter

from intelligence.llm_issue_extractor import (
    LLMIssueExtractor
)


# =========================
# CONFIG
# =========================

SAMPLE_SIZE = 50

INPUT_FILE = (
    "data/unknown_reviews.csv"
)

OUTPUT_FILE = (
    "data/llm_unknown_analysis.csv"
)


# =========================
# LOAD DATA
# =========================

df = pd.read_csv(
    INPUT_FILE
)

print(
    f"Loaded {len(df)} unknown reviews"
)

sample_df = df.sample(
    n=min(
        SAMPLE_SIZE,
        len(df)
    ),
    random_state=42
)



# =========================
# LLM
# =========================

extractor = (
    LLMIssueExtractor()
)

results = []

issue_counter = Counter()


# =========================
# ANALYSIS LOOP
# =========================

for idx, row in sample_df.iterrows():

    review_text = str(
        row["review_text"]
    )

    print(
        f"koko\n[{len(results)+1}/{len(sample_df)}]"
    )

    try:

        response = (
            extractor.extract(
                review_text
            )
        )

        issues = []

        if isinstance(
            response,
            str
        ):

            response = json.loads(
                response
            )

        if (
            isinstance(
                response,
                dict
            )
            and "issues" in response
        ):

            for issue in (
                response["issues"]
            ):

                issue_id = issue.get(
                    "issue_id",
                    "UNKNOWN"
                )

                issues.append(
                    issue_id
                )

                issue_counter[
                    issue_id
                ] += 1

        results.append({

            "review_text":
            review_text,

            "issues":
            "|".join(
                issues
            )
        })

    except Exception as e:

        print(
            f"ERROR: {e}"
        )

        results.append({

            "review_text":
            review_text,

            "issues":
            "ERROR"
        })


# =========================
# SAVE RESULTS
# =========================

results_df = pd.DataFrame(
    results
)

results_df.to_csv(

    OUTPUT_FILE,

    index=False
)

print(
    f"\nSaved results to {OUTPUT_FILE}"
)


# =========================
# ISSUE SUMMARY
# =========================

print("\n")
print("=" * 60)
print("ISSUE COUNTS")
print("=" * 60)

for issue, count in (
    issue_counter.most_common()
):

    print(
        f"{issue}: {count}"
    )