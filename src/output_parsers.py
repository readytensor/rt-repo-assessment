from typing import Type
from pydantic import BaseModel, Field, create_model
from generators import content_based_criterion_generator


class CriterionScoring(BaseModel):
    """
    Model for storing the scoring result of a single criterion.

    Attributes:
        score (int): The binary score for the criterion. 0 if the criterion is not met, 1 if it is met.
        explanation (str): The explanation for the score.
    """

    score: int = Field(
        description="The binary score for the criterion. 0 if the criterion is not met, 1 if it is met."
    )
    explanation: str = Field(description="The explanation for the score")


def get_content_based_scoring_model(
    input_file_extension: str = None,
) -> Type[BaseModel]:
    """
    Dynamically creates a Pydantic model for content-based scoring based on file extension.

    This function generates a model structure that can validate and store scores for
    various code quality criteria that are applicable to the given file extension.

    Args:
        input_file_extension (str, optional): The file extension to filter criteria by.
            If None, all criteria will be included. Defaults to None.

    Returns:
        Type[BaseModel]: A dynamically created Pydantic model with nested structure
        for storing and validating code quality scores.
    """
    scores_fields = {}
    for criterion_id, criterion in content_based_criterion_generator(
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
