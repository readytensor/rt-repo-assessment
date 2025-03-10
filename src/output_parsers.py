from typing import Any, Dict, List
from pydantic import BaseModel, Field


class CriterionScoring(BaseModel):
    score: int = Field(
        description="The binary score for the criterion. 0 if the criterion is not met, 1 if it is met."
    )
    explanation: str = Field(description="The explanation for the score")
