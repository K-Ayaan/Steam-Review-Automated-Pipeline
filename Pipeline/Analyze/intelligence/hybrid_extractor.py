from intelligence.rule_engine import (
    RuleEngine
)

from intelligence.llm_issue_extractor import (
    LLMIssueExtractor
)


class HybridExtractor:

    def __init__(self):

        self.rules = (
            RuleEngine()
        )

        self.llm = (
            LLMIssueExtractor()
        )

    def extract(

        self,

        review

    ):

        rule_result = (

            self.rules.extract(
                review
            )
        )        

        if len(rule_result) > 0:
            
            return {

                "issues":
                rule_result
            }
        return (

            self.llm.extract(
                review
            )
        )