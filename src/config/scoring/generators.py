from typing import List
from config import paths
from utils.general import read_yaml_file

CODE_QUALITY_CRITERIA = read_yaml_file(paths.CODE_QUALITY_CRITERIA_FPATH)
DEPENDENCIES_CRITERIA = read_yaml_file(paths.DEPENDANCIES_CRITERIA_FPATH)
LICENSE_CRITERIA = read_yaml_file(paths.LICENSE_CRITERIA_FPATH)
STRUCTURE_CRITERIA = read_yaml_file(paths.STRUCTURE_CRITERIA_FPATH)


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


def get_code_criteria_aggregation_logic():
    aggregation_logic = {}
    for category in CODE_QUALITY_CRITERIA.keys():
        for sub_category in CODE_QUALITY_CRITERIA[category].keys():
            for criterion_id in CODE_QUALITY_CRITERIA[category][sub_category].keys():
                logic = CODE_QUALITY_CRITERIA[category][sub_category][criterion_id][
                    "aggregation"
                ]
                aggregation_logic[criterion_id] = logic
    return aggregation_logic
