class UTMGenerator:

    def generate(

        self,

        audience,

        channel,

        game_name
    ):

        utm_source = (

            channel

            .lower()

            .replace(" ", "_")
        )

        utm_medium = "community"

        utm_campaign = (

            game_name

            .lower()

            .replace(" ", "_")

            +

            "_"

            +

            audience

            .lower()

            .replace(" ", "_")
        )

        return {

            "utm_source":
            utm_source,

            "utm_medium":
            utm_medium,

            "utm_campaign":
            utm_campaign
        }