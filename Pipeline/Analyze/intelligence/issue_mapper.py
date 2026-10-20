import json
import pandas as pd


class IssueMapper:

    def __init__(
        self,
        input_file,
        ontology_file
    ):

        self.df = pd.read_csv(
            input_file
        )

        with open(
            ontology_file,
            "r",
            encoding="utf-8"
        ) as f:

            self.ontology = json.load(f)

    def find_issues(
        self,
        text
    ):

        text = str(text).lower()

        found = []

        for issue_name, issue_data in (
            self.ontology.items()
        ):

            for keyword in issue_data[
                "keywords"
            ]:

                if keyword.lower() in text:

                    found.append(
                        issue_name
                    )

                    break

        if not found:

            found.append(
                "UNKNOWN"
            )

        return "|".join(found)

    def process(self):

        self.df["issues"] = (
            self.df[
                "clean_review_text"
            ]
            .apply(
                self.find_issues
            )
        )

        return self.df