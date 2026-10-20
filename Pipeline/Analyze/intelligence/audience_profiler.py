class AudienceProfiler:
    
    def profile(

        self,

        # game_name,

        report,

        genre_profile

    ):

        audiences = set(

            genre_profile.get(

                "target_audiences",

                []
            )
        )

        genre = genre_profile.get(

            "genre",

            "Unknown"
        )

        issue_counts = {

            issue["issue_id"]: issue["count"]

            for issue in report
        }

        multiplayer_score = (

            issue_counts.get(
                "MULTIPLAYER_FUN",
                0
            )

            +

            issue_counts.get(
                "MULTIPLAYER_CONNECTIVITY",
                0
            )
        )

        community_score = (

            issue_counts.get(
                "COMMUNITY_TOXICITY",
                0
            )
        )

        replay_score = (

            issue_counts.get(
                "REPLAYABILITY",
                0
            )
        )


        # Generic audiences

        if multiplayer_score >= 5:

            audiences.add(
                "Co-op Players"
            )

            audiences.add(
                "Friend Groups"
            )

        if replay_score >= 5:

            audiences.add(

                "Long-Term Players"
            )

        if community_score >= 5:

            audiences.update([

                "Competitive Players",

                "Ranked Players"
            ])

        return list(
            set(audiences)
        )