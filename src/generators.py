from typing import List, Optional, Dict, Tuple, Generator, Any
from config import paths
from utils.general import read_yaml_file

CODE_QUALITY_CRITERIA = read_yaml_file(paths.CODE_QUALITY_CRITERIA_FPATH)
DEPENDENCIES_CRITERIA = read_yaml_file(paths.DEPENDANCIES_CRITERIA_FPATH)
LICENSE_CRITERIA = read_yaml_file(paths.LICENSE_CRITERIA_FPATH)
STRUCTURE_CRITERIA = read_yaml_file(paths.STRUCTURE_CRITERIA_FPATH)
DOCUMENTATION_CRITERIA = read_yaml_file(paths.DOCUMENTATION_CRITERIA_FPATH)

ALL_CRITERIA = [
    CODE_QUALITY_CRITERIA,
    DEPENDENCIES_CRITERIA,
    LICENSE_CRITERIA,
    STRUCTURE_CRITERIA,
    DOCUMENTATION_CRITERIA,
]


def criteria_generator(
    criteria: Dict[str, Any],
) -> Generator[Tuple[str, Dict[str, Any]], None, None]:
    """
    Generate criterion ID and criterion details from a criteria dictionary.

    Args:
        criteria: Dictionary containing categories, subcategories, and criteria

    Returns:
        Generator yielding tuples of (criterion_id, criterion_details)
    """
    for category in criteria.keys():
        for sub_category in criteria[category].keys():
            for criterion_id in criteria[category][sub_category].keys():
                yield criterion_id, criteria[category][sub_category][criterion_id]


def code_quality_criterion_generator(
    input_file_extension: Optional[str] = None,
) -> Generator[Tuple[str, Dict[str, Any]], None, None]:
    """
    Generate code quality criteria filtered by file extension.

    Args:
        input_file_extension: Optional file extension to filter criteria by

    Returns:
        Generator yielding tuples of (criterion_id, criterion_details) for code quality criteria
    """
    for criterion_id, criterion in criteria_generator(CODE_QUALITY_CRITERIA):
        included_file_extensions = criterion.get("include_extensions", None)
        excluded_file_extensions = criterion.get("exclude_extensions", None)

        if (
            input_file_extension
            and included_file_extensions
            and input_file_extension not in included_file_extensions
        ):
            continue
        if (
            input_file_extension
            and excluded_file_extensions
            and input_file_extension in excluded_file_extensions
        ):
            continue

        yield criterion_id, criterion


def content_based_criterion_generator(
    input_file_extension: Optional[str] = None,
) -> Generator[Tuple[str, Dict[str, Any]], None, None]:
    """
    Generate content-based criteria from all criteria types, filtered by file extension.

    Args:
        input_file_extension: Optional file extension to filter criteria by

    Returns:
        Generator yielding tuples of (criterion_id, criterion_details) for content-based criteria
    """
    for criteria in ALL_CRITERIA:
        for criterion_id, criterion in criteria_generator(criteria):
            if criterion.get("based_on") != "file_content":
                continue

            included_file_extensions = criterion.get("include_extensions", None)
            excluded_file_extensions = criterion.get("exclude_extensions", None)

            if (
                input_file_extension
                and included_file_extensions
                and input_file_extension not in included_file_extensions
            ):
                continue
            if (
                input_file_extension
                and excluded_file_extensions
                and input_file_extension in excluded_file_extensions
            ):
                continue

            yield criterion_id, criterion


def metadata_based_criterion_generator() -> (
    Generator[Tuple[str, Dict[str, Any]], None, None]
):
    """
    Generate metadata-based criteria from all criteria types.

    Returns:
        Generator yielding tuples of (criterion_id, criterion_details) for metadata-based criteria
    """
    for criteria in ALL_CRITERIA:
        for criterion_id, criterion in criteria_generator(criteria):
            if criterion.get("based_on", "metadata") != "metadata":
                continue
            yield criterion_id, criterion


def logic_based_criterion_generator() -> (
    Generator[Tuple[str, Dict[str, Any]], None, None]
):
    """
    Generate custom logic-based criteria from all criteria types.

    Returns:
        Generator yielding tuples of (criterion_id, criterion_details) for custom logic-based criteria
    """
    for criteria in ALL_CRITERIA:
        for criterion_id, criterion in criteria_generator(criteria):
            if criterion.get("based_on") != "custom_logic":
                continue
            yield criterion_id, criterion


def documentation_criterion_generator() -> (
    Generator[Tuple[str, Dict[str, Any]], None, None]
):
    """
    Generate documentation criteria.

    Returns:
        Generator yielding tuples of (criterion_id, criterion_details) for documentation criteria
    """
    for criterion_id, criterion in criteria_generator(DOCUMENTATION_CRITERIA):
        yield criterion_id, criterion


def dependancies_criterion_generator() -> (
    Generator[Tuple[str, Dict[str, Any]], None, None]
):
    """
    Generate dependencies criteria.

    Returns:
        Generator yielding tuples of (criterion_id, criterion_details) for dependencies criteria
    """
    for criterion_id, criterion in criteria_generator(DEPENDENCIES_CRITERIA):
        yield criterion_id, criterion


def license_criterion_generator() -> Generator[Tuple[str, Dict[str, Any]], None, None]:
    """
    Generate license criteria.

    Returns:
        Generator yielding tuples of (criterion_id, criterion_details) for license criteria
    """
    for criterion_id, criterion in criteria_generator(LICENSE_CRITERIA):
        yield criterion_id, criterion


def structure_criterion_generator() -> (
    Generator[Tuple[str, Dict[str, Any]], None, None]
):
    """
    Generate structure criteria.

    Returns:
        Generator yielding tuples of (criterion_id, criterion_details) for structure criteria
    """
    for criterion_id, criterion in criteria_generator(STRUCTURE_CRITERIA):
        yield criterion_id, criterion


def get_aggregation_logic() -> Dict[str, str]:
    """
    Get the aggregation logic for all criteria.

    Returns:
        Dictionary mapping criterion IDs to their aggregation logic (e.g., 'AND', 'OR')
    """
    aggregation_logic = {}
    for criteria in ALL_CRITERIA:
        for criterion_id, criterion in criteria_generator(criteria):
            if "aggregation" not in criterion:
                continue
            logic = criterion["aggregation"]
            aggregation_logic[criterion_id] = logic
    return aggregation_logic


def get_criteria_by_type() -> Dict[str, List[str]]:
    """
    Categorize criteria by their type (Essential, Professional, Elite).

    Returns:
        Dictionary with keys 'Essential', 'Professional', 'Elite' and values as lists of criterion IDs
    """
    result = {
        "Essential": [],
        "Professional": [],
        "Elite": [],
    }
    for criteria in ALL_CRITERIA:
        for criterion_id, criterion in criteria_generator(criteria):
            if criterion.get("essential", False):
                result["Essential"].append(criterion_id)
            if criterion.get("professional", False):
                result["Professional"].append(criterion_id)
            if criterion.get("elite", False):
                result["Elite"].append(criterion_id)
    return result


def get_criteria_names() -> Dict[str, str]:
    """
    Get the display names for all criteria.

    Returns:
        Dictionary mapping criterion IDs to their display names
    """
    result = {}
    for criteria in ALL_CRITERIA:
        for criterion_id, criterion in criteria_generator(criteria):
            result[criterion_id] = criterion["name"]
    return result


def get_category_criteria() -> Dict[str, List[str]]:
    """
    Group criteria by their top-level category.

    Returns:
        Dictionary mapping category names to lists of criterion IDs
    """
    result = {}
    for criteria in ALL_CRITERIA:
        for category in criteria.keys():
            result[category] = []
            for sub_category in criteria[category].keys():
                result[category].extend(list(criteria[category][sub_category].keys()))

    return result


def get_instructions(
    criterion_id: Optional[str] = None,
    content_based_only: bool = False,
    metadata_based_only: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """
    Get instructions for criteria, with optional filtering.

    Args:
        criterion_id: Optional specific criterion ID to get instructions for
        content_based_only: If True, only return content-based criteria
        metadata_based_only: If True, only return metadata-based criteria

    Returns:
        Dictionary mapping criterion IDs to their instructions and names

    Raises:
        ValueError: If both content_based_only and metadata_based_only are True
    """
    if content_based_only and metadata_based_only:
        raise ValueError(
            "content_based_only and metadata_based_only cannot both be True"
        )
    result = {}
    for criteria in ALL_CRITERIA:
        for criterion_id_iter, criterion in criteria_generator(criteria):
            if criterion_id and criterion_id_iter != criterion_id:
                continue

            if criterion_id and criterion_id_iter == criterion_id:
                return {
                    "criterion name": criterion["name"],
                    "instructions": criterion.get("instructions", None),
                }

            # Filter based on content_based or logic_based parameters
            is_content_based = criterion.get("based_on", "metadata") == "file_content"

            # Skip if content_based_only is True but criterion is not content-based
            if content_based_only and not is_content_based:
                continue

            # Skip if logic_based_only is True but criterion is content-based
            if metadata_based_only and is_content_based:
                continue

            instructions = criterion.get("instructions", None)
            if instructions:
                result[criterion_id_iter] = {
                    "criterion name": criterion["name"],
                    "instructions": instructions,
                }
    return result


def get_criteria_args() -> Dict[str, Dict[str, Any]]:
    """
    Get arguments for logic-based criteria.

    Returns:
        Dictionary mapping criterion IDs to their arguments
    """
    result = {}
    for criterion_id, criterion in logic_based_criterion_generator():
        result[criterion_id] = criterion.get("args", {})
    return result
