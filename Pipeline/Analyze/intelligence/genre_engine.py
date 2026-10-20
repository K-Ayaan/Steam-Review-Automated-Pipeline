import json


class GenreEngine:

    def __init__(self):

        with open(

            "config/game_profiles.json",

            "r",

            encoding="utf-8"

        ) as f:

            self.profiles = json.load(f)

    def detect(

        self,

        game_name
    ):

        return self.profiles.get(

            game_name,

            {

                "genre":
                "Unknown",

                "pillars":
                [],

                "target_audiences":
                []
            }
        )