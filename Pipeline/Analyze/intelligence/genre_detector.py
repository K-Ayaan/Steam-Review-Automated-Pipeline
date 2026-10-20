class GenreDetector:

    def detect(

        self,

        game_name,

        # report

    ):

        game = game_name.lower()

        if any(

            x in game

            for x in [

                "counter-strike",

                "cs2",

                "valorant"
            ]
        ):

            return "FPS"

        if any(

            x in game

            for x in [

                "valheim",

                "rust",

                "ark"
            ]
        ):

            return "SURVIVAL"

        if any(

            x in game

            for x in [

                "backrooms",

                "cursed",

                "phasmophobia",

                "ghost"
            ]
        ):

            return "HORROR"

        return "UNKNOWN"