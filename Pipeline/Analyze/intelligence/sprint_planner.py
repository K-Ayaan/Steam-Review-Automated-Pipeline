class SprintPlanner:

    def plan(self, issue):

        issue_id = issue["issue_id"]

        plans = {

            "BUGS": {

                "priority": "P1",

                "story_points": 13,

                "impact": "+6 Review Score",

                "tasks": [

                    "Fix critical gameplay bugs",

                    "Fix interaction failures",

                    "Fix progression blockers"
                ]
            },

            "CRASHES": {

                "priority": "P1",

                "story_points": 21,

                "impact": "+10 Review Score",

                "tasks": [

                    "Analyze crash logs",

                    "Fix startup crashes",

                    "Fix memory leaks"
                ]
            },

            "PERFORMANCE_FPS": {

                "priority": "P1",

                "story_points": 13,

                "impact": "+8 Review Score",

                "tasks": [

                    "Profile rendering pipeline",

                    "Reduce draw calls",

                    "Optimize shaders"
                ]
            },

            "MULTIPLAYER_CONNECTIVITY": {

                "priority": "P1",

                "story_points": 13,

                "impact": "+7 Review Score",

                "tasks": [

                    "Investigate lobby joins",

                    "Fix invite system",

                    "Improve reconnect logic"
                ]
            },

            "GAMEPLAY_CLARITY": {

                "priority": "P2",

                "story_points": 8,

                "impact": "+5 Review Score",

                "tasks": [

                    "Improve objectives",

                    "Improve player guidance",

                    "Reduce confusion"
                ]
            }
        }

        return plans.get(

            issue_id,

            {

                "priority": "P3",

                "story_points": 5,

                "impact": "+2 Review Score",

                "tasks": [

                    "Investigate issue"
                ]
            }
        )