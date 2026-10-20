from intelligence.ad_generator import (
    AdGenerator
)


class CreativeGenerator:

    def __init__(self):

        self.ad_generator = (
            AdGenerator()
        )

    def generate(

        self,

        campaign,

        marketing_report,

        genre_profile,

        game_name,
        
    ):

        audience = campaign[
            "audience"
        ]

        channel = campaign[
            "channel"
        ]

        # game_name= campaign.get("game_name", [])
        # game_name= genre_profile.get("game_name", [])
        # game_name= genre_profile["game_name"]

        # prompt_context = {

        #     "game_name":
        #     game_name,

        #     "audience":
        #     audience,

        #     "channel":
        #     channel,

        #     "genre":
        #     genre_profile[
        #         "genre"
        #     ],

        #     "pillars":
        #     genre_profile[
        #         "pillars"
        #     ],

        #     # "promote":
        #     # marketing_report[
        #     #     "promote"
        #     # ],

        #     # "promote": {marketing_report.get("angles,[]")},
        #     "promote": campaign["promote"],

        #     # "avoid":
        #     # marketing_report[
        #     #     "avoid"
        #     # ],

        #     "avoid": {marketing_report.get("avoid,[]")},
        # }

        prompt_context = {

            "game_name":
            game_name,

            "genre":
            genre_profile["genre"],

            "audience":
            campaign["audience"],

            "platform":
            campaign["platform"],

            "promote":
            campaign["promote"],

            "avoid":
            marketing_report["avoid"],

            "pillars":
            genre_profile["pillars"]
        }

        return self.ad_generator.generate_creatives(

            prompt_context
        )