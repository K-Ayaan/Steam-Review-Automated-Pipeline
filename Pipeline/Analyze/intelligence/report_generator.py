from intelligence.severity_engine import (
    SeverityEngine
)

from ontology.issue_catalog import (
    ISSUE_CATALOG
)

from intelligence.business_impact_engine import (
    BusinessImpactEngine
)


class ReportGenerator:

    def __init__(self):

        self.severity_engine = (
            SeverityEngine()
        )

        self.business_engine = (
            BusinessImpactEngine()
        )

    def generate(
        self,
        issue_database,
        known_reviews,
        game_name=None
    ):

        report = []

        for issue_id, data in (
            issue_database.items()
        ):

            if issue_id == "NO_ISSUE":
                continue

            catalog_data = ISSUE_CATALOG.get(

                issue_id,

                {

                    "department":
                    "Unknown",

                    "team":
                    "Unknown",

                    "priority":
                    "P3",

                    "category":
                    "Unknown"
                }
            )

            severity_result = (

                self.severity_engine.calculate(

                    issue_id,

                    data,

                    known_reviews
                )
            )

            top_player_segment = max(

                data["player_segments"],

                key=data["player_segments"].get
            )

            business_impact = (

                self.business_engine.calculate(

                    {

                        "count":
                        data["count"],

                        "impact_score":
                        data["impact_score"],

                        "helpful_count":
                        data["helpful_count"],

                        "top_player_segment":
                        top_player_segment
                    }
                )
            )

            # print("==========================")
            # print(
            #     issue_id,
            #     severity_result["score"]
            # )
            # print("=========================")

            report.append({

                "game_name":
                game_name,  

                "issue_id":
                issue_id,

                "count":
                data["count"],

                "impact_score":
                data["impact_score"],

                "helpful_count":
                data["helpful_count"],

                "severity":
                severity_result["severity"],

                "ranking_score":
                severity_result["score"],

                "department":
                catalog_data["department"],

                "team":
                catalog_data["team"],

                "priority":
                catalog_data["priority"],

                "category":
                catalog_data["category"],

                "top_language":
                max(
                    data["languages"],
                    key=data["languages"].get
                ),

                "top_player_segment":
                top_player_segment,

                "business_impact":
                business_impact,

                "signal_type":
                catalog_data.get(
                    "signal_type",
                    "negative"
                ),
            })

        # for issue in report:

        #     issue["ranking_score"] = (

        #         issue["count"] * 5

        #         +

        #         issue["impact_score"]

        #         +

        #         issue["helpful_count"]
        #     )

        report = sorted(

            report,

            key=lambda x:

                x["ranking_score"],

            reverse=True
        )

        total_issues = len(report)

        for idx, issue in enumerate(report):

            percentile = (

                idx + 1

            ) / total_issues

            if percentile <= 0.10:

                issue["severity"] = "CRITICAL"

            elif percentile <= 0.30:

                issue["severity"] = "HIGH"

            elif percentile <= 0.60:

                issue["severity"] = "MEDIUM"

            else:

                issue["severity"] = "LOW"
        

        return report