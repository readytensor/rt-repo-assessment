from typing import List
from config import paths
from utils.general import read_yaml_file

CODE_QUALITY_CRITERIA = read_yaml_file(paths.CODE_QUALITY_CRITERIA_FPATH)
DEPENDENCIES_CRITERIA = read_yaml_file(paths.DEPENDANCIES_CRITERIA_FPATH)
LICENSE_CRITERIA = read_yaml_file(paths.LICENSE_CRITERIA_FPATH)
STRUCTURE_CRITERIA = read_yaml_file(paths.STRUCTURE_CRITERIA_FPATH)
DOCUMENTATION_CRITERIA = read_yaml_file(paths.DOCUMENTATION_CRITERIA_FPATH)


def code_quality_criterion_generator(input_file_extension: str = None):
    for category in CODE_QUALITY_CRITERIA.keys():
        for sub_category in CODE_QUALITY_CRITERIA[category].keys():
            for criterion_id in CODE_QUALITY_CRITERIA[category][sub_category].keys():
                included_file_extensions = CODE_QUALITY_CRITERIA[category][
                    sub_category
                ][criterion_id].get("include_extensions", None)
                excluded_file_extensions = CODE_QUALITY_CRITERIA[category][
                    sub_category
                ][criterion_id].get("exclude_extensions", None)

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

                yield criterion_id, CODE_QUALITY_CRITERIA[category][sub_category][
                    criterion_id
                ]


def content_based_criterion_generator(input_file_extension: str = None):
    for criteria in [
        CODE_QUALITY_CRITERIA,
        DEPENDENCIES_CRITERIA,
        LICENSE_CRITERIA,
        STRUCTURE_CRITERIA,
        DOCUMENTATION_CRITERIA,
    ]:
        for category in criteria.keys():
            for sub_category in criteria[category].keys():
                for criterion_id in criteria[category][sub_category].keys():
                    if not criteria[category][sub_category][criterion_id].get(
                        "content_based", False
                    ):
                        continue

                    included_file_extensions = criteria[category][sub_category][
                        criterion_id
                    ].get("include_extensions", None)
                    excluded_file_extensions = criteria[category][sub_category][
                        criterion_id
                    ].get("exclude_extensions", None)

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

                    yield criterion_id, criteria[category][sub_category][criterion_id]


def documentation_criterion_generator():
    for category in DOCUMENTATION_CRITERIA.keys():
        for sub_category in DOCUMENTATION_CRITERIA[category].keys():
            for criterion_id in DOCUMENTATION_CRITERIA[category][sub_category].keys():
                yield criterion_id, DOCUMENTATION_CRITERIA[category][sub_category][
                    criterion_id
                ]


def dependancies_criterion_generator():
    for category in DEPENDENCIES_CRITERIA.keys():
        for sub_category in DEPENDENCIES_CRITERIA[category].keys():
            for criterion_id in DEPENDENCIES_CRITERIA[category][sub_category].keys():
                yield criterion_id, DEPENDENCIES_CRITERIA[category][sub_category][
                    criterion_id
                ]


def license_criterion_generator():
    for category in LICENSE_CRITERIA.keys():
        for sub_category in LICENSE_CRITERIA[category].keys():
            for criterion_id in LICENSE_CRITERIA[category][sub_category].keys():
                yield criterion_id, LICENSE_CRITERIA[category][sub_category][
                    criterion_id
                ]


def structure_criterion_generator():
    for category in STRUCTURE_CRITERIA.keys():
        for sub_category in STRUCTURE_CRITERIA[category].keys():
            for criterion_id in STRUCTURE_CRITERIA[category][sub_category].keys():
                yield criterion_id, STRUCTURE_CRITERIA[category][sub_category][
                    criterion_id
                ]


def get_aggregation_logic():
    aggregation_logic = {}
    for criteria in [
        CODE_QUALITY_CRITERIA,
        DEPENDENCIES_CRITERIA,
        LICENSE_CRITERIA,
        STRUCTURE_CRITERIA,
        DOCUMENTATION_CRITERIA,
    ]:
        for category in criteria.keys():
            for sub_category in criteria[category].keys():
                for criterion_id in criteria[category][sub_category].keys():
                    if (
                        "aggregation"
                        not in criteria[category][sub_category][criterion_id]
                    ):
                        continue
                    logic = criteria[category][sub_category][criterion_id][
                        "aggregation"
                    ]
                    aggregation_logic[criterion_id] = logic
    return aggregation_logic


def get_criteria_by_type():
    result = {
        "Essential": [],
        "Professional": [],
        "Elite": [],
    }
    for criteria in [
        CODE_QUALITY_CRITERIA,
        DEPENDENCIES_CRITERIA,
        LICENSE_CRITERIA,
        STRUCTURE_CRITERIA,
    ]:
        for category in criteria.keys():
            for sub_category in criteria[category].keys():
                for criterion_id in criteria[category][sub_category].keys():
                    if criteria[category][sub_category][criterion_id].get(
                        "essential", False
                    ):
                        result["Essential"].append(criterion_id)
                    if criteria[category][sub_category][criterion_id].get(
                        "professional", False
                    ):
                        result["Professional"].append(criterion_id)
                    if criteria[category][sub_category][criterion_id].get(
                        "elite", False
                    ):
                        result["Elite"].append(criterion_id)
    return result


def get_criteria_names():
    result = {}
    for criteria in [
        CODE_QUALITY_CRITERIA,
        DEPENDENCIES_CRITERIA,
        LICENSE_CRITERIA,
        STRUCTURE_CRITERIA,
        DOCUMENTATION_CRITERIA,
    ]:
        for category in criteria.keys():
            for sub_category in criteria[category].keys():
                for criterion_id in criteria[category][sub_category].keys():
                    result[criterion_id] = criteria[category][sub_category][
                        criterion_id
                    ]["name"]
    return result


def get_category_criteria():
    result = {}
    for criteria in [
        CODE_QUALITY_CRITERIA,
        DEPENDENCIES_CRITERIA,
        LICENSE_CRITERIA,
        STRUCTURE_CRITERIA,
        DOCUMENTATION_CRITERIA,
    ]:
        for category in criteria.keys():
            result[category] = []
            for sub_category in criteria[category].keys():
                result[category].extend(list(criteria[category][sub_category].keys()))
    return result


def get_instructions(
    criterion_id: str = None,
    content_based_only: bool = False,
    metadata_based_only: bool = False,
):
    if content_based_only and metadata_based_only:
        raise ValueError(
            "content_based_only and metadata_based_only cannot both be True"
        )
    result = {}
    for criteria in [
        CODE_QUALITY_CRITERIA,
        DEPENDENCIES_CRITERIA,
        LICENSE_CRITERIA,
        STRUCTURE_CRITERIA,
        DOCUMENTATION_CRITERIA,
    ]:
        for category in criteria.keys():
            for sub_category in criteria[category].keys():
                for id in criteria[category][sub_category].keys():
                    criterion = criteria[category][sub_category][id]

                    if criterion_id and id != criterion_id:
                        continue

                    if criterion_id and id == criterion_id:
                        return {
                            "criterion name": criterion["name"],
                            "instructions": criterion.get("instructions", None),
                        }

                    # Filter based on content_based or logic_based parameters

                    # Filter based on content_based or logic_based parameters
                    is_content_based = criterion.get("content_based", False)

                    # Skip if content_based_only is True but criterion is not content-based
                    if content_based_only and not is_content_based:
                        continue

                    # Skip if logic_based_only is True but criterion is content-based
                    if metadata_based_only and is_content_based:
                        continue

                    instructions = criterion.get("instructions", None)
                    if instructions:
                        result[id] = {
                            "criterion name": criterion["name"],
                            "instructions": instructions,
                        }
    return result
