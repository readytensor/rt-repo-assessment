from functools import wraps
from typing import Dict, Any, Callable, TypeVar, Protocol


class ScoringResult(Protocol):
    score: int
    explanation: str


def validate_scoring_result(result: Dict[str, Any]) -> None:
    """Validate that the scoring result has the required fields."""
    if not isinstance(result, dict):
        raise TypeError("Scoring result must be a dictionary")
    if "score" not in result:
        raise KeyError("Scoring result must contain a 'score' key")
    if "explanation" not in result:
        raise KeyError("Scoring result must contain an 'explanation' key")
    if not isinstance(result["score"], (int, float)):
        raise TypeError("Score must be a number")
    if not isinstance(result["explanation"], str):
        raise TypeError("Explanation must be a string")


F = TypeVar("F", bound=Callable[..., Dict[str, Any]])


def scoring_function(func: F) -> F:
    """Decorator to ensure scoring functions return the expected structure."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        result = func(*args, **kwargs)
        validate_scoring_result(result)
        return result

    return wrapper


@scoring_function
def readme_presence(metadata: Dict[str, Any]) -> Dict[str, Any]:
    if metadata["readme_exists"]:
        score = 1
        explanation = "The root directory contains a README.md file."
    else:
        score = 0
        explanation = "The root directory does not contain a README.md file."

    return {
        "score": score,
        "explanation": explanation,
    }


@scoring_function
def script_length(metadata: Dict[str, Any], max_script_length: int) -> Dict[str, Any]:
    """
    Check if scripts in the repository exceed the maximum allowed length.

    Args:
        metadata (Dict[str, Any]): Repository metadata containing script lengths.
        max_script_length (int): Maximum allowed length for scripts in lines.

    Returns:
        Dict[str, Any]: Dictionary containing score (1 if all scripts are within
        the length limit, 0 otherwise) and an explanation.
    """
    script_lengths = metadata["script_lengths"]
    long_scripts = []
    score = 1
    explanation = "All scripts are less than 500 lines."
    for script, length in script_lengths.items():
        if length > max_script_length:
            score = 0
            long_scripts.append(script)
            explanation = f"The following scripts are longer than {max_script_length} lines: {long_scripts}"

    return {
        "score": score,
        "explanation": explanation,
    }


logic_based_scoring = {
    "readme_presence": readme_presence,
    "script_length": script_length,
}
