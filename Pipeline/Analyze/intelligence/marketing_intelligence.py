class MarketingIntelligence:

    def generate(

        self,

        audience_report,

        known_reviews,

        genre_profile

    ):

        strengths = (

            audience_report[
                "strengths"
            ]
        )

        weaknesses = (

            audience_report[
                "weaknesses"
            ]
        )

        allowed_pillars = (

            genre_profile.get(

                "pillars",

                []
            )
        )

        angles = []

        avoid = []

        horror_mentions = 0

        for issue in audience_report.get(

            "report",

            []

        ):

            if issue["issue_id"] in [

                "HORROR_EXPERIENCE",

                "HORROR_EFFECTIVENESS"

            ]:

                horror_mentions += (

                    issue["count"]
                )


        if (

            "Fear"

            in allowed_pillars

        ):

            if horror_mentions >= 3:

                angles.append(

                    "Horror Atmosphere"
                )

        if (

            "Immersion"

            in allowed_pillars

            and

            "IMMERSION"

            in strengths

        ):

            angles.append(

                "Immersive Gameplay"
            )

        if (

            "Team Play"

            in allowed_pillars

            and

            "MULTIPLAYER_FUN"

            in strengths

        ):

            angles.append(
                "Co-op Experience"
            )

        if (

            "BUGS"

            in weaknesses
        ):

            avoid.append(

                "Polished Experience"
            )

        if (

            "PERFORMANCE_FPS"

            in weaknesses
        ):

            avoid.append(

                "Graphics Performance"
            )

        if (

            genre_profile[
                "genre"
            ]

            ==

            "Competitive FPS"
        ):

            angles.extend([

                "Skill Expression",

                "Ranked Progression",

                "Competitive Play"
            ])

        elif (

            genre_profile[
                "genre"
            ]

            ==

            "Survival Crafting"
        ):

            angles.extend([

                "Exploration",

                "Building",

                "Progression"
            ])

        elif (

            genre_profile[
                "genre"
            ]

            ==

            "Co-op Horror"
        ):

            angles.extend([

                "Fear",

                "Horror Atmosphere",

                "Co-op Survival"
            ])
        

        return {

            "angles":

                angles,

            "avoid":

                avoid,

            "target_audiences":

                audience_report[
                    "target_audiences"
                ]
        }