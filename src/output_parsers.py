from typing import List, Dict
from pydantic import BaseModel, Field, create_model
from generators import code_quality_criterion_generator


class CriterionScoring(BaseModel):
    score: int = Field(
        description="The binary score for the criterion. 0 if the criterion is not met, 1 if it is met."
    )
    explanation: str = Field(description="The explanation for the score")


def get_code_quality_scoring_model(input_file_extension: str = None):

    scores_fields = {}
    for criterion_id, criterion in code_quality_criterion_generator(
        input_file_extension
    ):

        scores_fields[criterion_id] = (
            CriterionScoring,
            Field(description=f"Score for {criterion['description']}"),
        )

    # Create the Scores model
    CodeQualityScores = create_model("CodeQualityScores", **scores_fields)

    # Then create the main model with the nested Scores model
    field_definitions = {
        "scores": (CodeQualityScores, Field(description="All criteria scores")),
    }

    return create_model("CodeQualityFileScoring", **field_definitions)
