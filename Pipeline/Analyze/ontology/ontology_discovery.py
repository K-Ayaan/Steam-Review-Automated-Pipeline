import pandas as pd

from collections import Counter

import re


class OntologyDiscovery:

    def discover(

        self,

        csv_path,

        top_n=100

    ):

        df = pd.read_csv(
            csv_path
        )

        text = " ".join(

            df[
                "review_text"
            ].astype(str)

        )

        words = re.findall(

            r"\b[a-zA-Z]{4,}\b",

            text.lower()

        )

        stopwords = {

            "this",
            "that",
            "with",
            "from",
            "have",
            "game",
            "play",
            "played",
            "very",
            "good",
            "great",
            "just",
            "they",
            "them",
            "what",
            "when",
            "your"
        }

        words = [

            w

            for w in words

            if w not in stopwords
        ]

        return Counter(
            words
        ).most_common(
            top_n
        )