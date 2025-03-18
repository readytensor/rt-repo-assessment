from typing import List, Optional
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


def criteria_generator(criteria: dict):
    for category in criteria.keys():
        for sub_category in criteria[category].keys():
            for criterion_id in criteria[category][sub_category].keys():
                yield criterion_id, criteria[category][sub_category][criterion_id]


def code_quality_criterion_generator(input_file_extension: Optional[str] = None):
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


def content_based_criterion_generator(input_file_extension: Optional[str] = None):
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


def metadata_based_criterion_generator():
    for criteria in ALL_CRITERIA:
        for criterion_id, criterion in criteria_generator(criteria):
            if criterion.get("based_on", "metadata") != "metadata":
                continue
            yield criterion_id, criterion


def logic_based_criterion_generator():
    for criteria in ALL_CRITERIA:
        for criterion_id, criterion in criteria_generator(criteria):
            if criterion.get("based_on") != "custom_logic":
                continue
            yield criterion_id, criterion


def documentation_criterion_generator():
    for criterion_id, criterion in criteria_generator(DOCUMENTATION_CRITERIA):
        yield criterion_id, criterion


def dependancies_criterion_generator():
    for criterion_id, criterion in criteria_generator(DEPENDENCIES_CRITERIA):
        yield criterion_id, criterion


def license_criterion_generator():
    for criterion_id, criterion in criteria_generator(LICENSE_CRITERIA):
        yield criterion_id, criterion


def structure_criterion_generator():
    for criterion_id, criterion in criteria_generator(STRUCTURE_CRITERIA):
        yield criterion_id, criterion


def get_aggregation_logic():
    aggregation_logic = {}
    for criteria in ALL_CRITERIA:
        for criterion_id, criterion in criteria_generator(criteria):
            if "aggregation" not in criterion:
                continue
            logic = criterion["aggregation"]
            aggregation_logic[criterion_id] = logic
    return aggregation_logic


def get_criteria_by_type():
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


def get_criteria_names():
    result = {}
    for criteria in ALL_CRITERIA:
        for criterion_id, criterion in criteria_generator(criteria):
            result[criterion_id] = criterion["name"]
    return result


def get_category_criteria():
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
):
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


def get_criteria_args():
    result = {}
    for criterion_id, criterion in logic_based_criterion_generator():
        result[criterion_id] = criterion.get("args", {})
    return result
