import pandas as pd


class TopicClassifier:

    TOPICS = {

        "Bugs": [
            "bug",
            "bugs",
            "crash",
            "crashes",
            "glitch",
            "broken",
            "error"
        ],

        "Performance": [
            "lag",
            "fps",
            "stutter",
            "optimization",
            "performance"
        ],

        "Graphics": [
            "graphics",
            "visual",
            "texture",
            "lighting"
        ],

        "Gameplay": [
            "gameplay",
            "mechanic",
            "mechanics",
            "combat"
        ],

        "Audio": [
            "audio",
            "sound",
            "music",
            "voice"
        ],

        "Multiplayer": [
            "multiplayer",
            "coop",
            "co-op",
            "matchmaking",
            "lobby",
            "server"
        ],

        "Tutorial": [
            "tutorial",
            "guide",
            "learn",
            "instruction"
        ],

        "UI_UX": [
            "ui",
            "ux",
            "menu",
            "interface"
        ],

        "Content": [
            "content",
            "map",
            "maps",
            "level",
            "levels"
        ],

        "Controls": [
            "controls",
            "keybind",
            "mouse",
            "keyboard"
        ]
    }

    def __init__(self, input_file):

        self.df = pd.read_csv(input_file)

    def classify_review(self, text):

        text = str(text).lower()

        detected_topics = []

        for topic, keywords in self.TOPICS.items():

            if any(
                keyword in text
                for keyword in keywords
            ):
                detected_topics.append(topic)

        if not detected_topics:

            detected_topics.append(
                "Uncategorized"
            )

        return "|".join(
            detected_topics
        )

    def classify(self):

        self.df["topics"] = (
            self.df["clean_review_text"]
            .apply(
                self.classify_review
            )
        )

        return self.df

    def save(self, output_file):

        self.df.to_csv(
            output_file,
            index=False,
            encoding="utf-8-sig"
        )