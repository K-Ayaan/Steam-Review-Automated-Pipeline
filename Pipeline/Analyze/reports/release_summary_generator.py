class ReleaseSummaryGenerator:

    def generate(

        self,

        health,

        audience,

        campaign,

        impact
    ):

        summary = {}

        summary[
            "overall_health"
        ] = health[
            "overall_health"
        ]
        summary[
            "target_audiences"
        ] = audience.get(

            "target_audiences",

            []
        )
        summary[
            "recommended_channels"
        ] = campaign.get(

            "recommended_channels",

            []
        )
        summary[
            "promote"
        ] = campaign.get(

            "promote",

            []
        )

        improvements = []
        regressions = []
        for issue, data in (

            impact.items()
        ):

            if issue == "_comparison":

                continue

            change = data.get(

                "change_percent",

                0
            )

            if change < 0:

                improvements.append({

                    "issue":
                    issue,

                    "change":
                    change
                })

            elif change > 0:

                regressions.append({

                    "issue":
                    issue,

                    "change":
                    change
                })

        improvements = sorted(

            improvements,

            key=lambda x:
            x["change"]
        )[:5]

        regressions = sorted(

            regressions,

            key=lambda x:
            x["change"],

            reverse=True
        )[:5]

        summary[
            "top_improvements"
        ] = improvements

        summary[
            "top_regressions"
        ] = regressions

        return summary
