from functools import wraps
from typing import Dict, Any, Callable, TypeVar, Protocol


class ScoringResult(Protocol):
    """Protocol defining the structure of a scoring result.

    Attributes:
        score (int): The numeric score assigned (typically 0 or 1).
        explanation (str): A human-readable explanation of the score.
    """

    score: int
    explanation: str


def validate_scoring_result(result: Dict[str, Any]) -> None:
    """Validate that the scoring result has the required fields.

    Args:
        result (Dict[str, Any]): The scoring result to validate.

    Raises:
        TypeError: If the result is not a dictionary or if score is not a number or explanation is not a string.
        KeyError: If the result does not contain 'score' or 'explanation' keys.
    """
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


def scoring_function(func: F) -> Callable[..., Dict[str, Any]]:
    """Decorator to ensure scoring functions return the expected structure.

    Args:
        func (F): The scoring function to decorate.

    Returns:
        Callable[..., Dict[str, Any]]: The decorated function that validates its return value.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Dict[str, Any]:
        result = func(*args, **kwargs)
        validate_scoring_result(result)
        return result

    return wrapper


@scoring_function
def readme_presence(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Check if a README.md file exists in the root directory.

    Args:
        metadata (Dict[str, Any]): Repository metadata containing readme existence information.

    Returns:
        Dict[str, Any]: Dictionary containing score (1 if README exists, 0 otherwise) and an explanation.
    """
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
