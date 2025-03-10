from config import paths
from utils.general import read_yaml_file


def code_quality_criterion_generator():
    criteria = read_yaml_file(paths.CODE_QUALITY_CRITERIA_FPATH)
    for category in criteria.keys():
        for sub_category in criteria[category].keys():
            for criterion_id in criteria[category][sub_category].keys():
                yield criterion_id, criteria[category][sub_category][criterion_id]


def dependancies_criterion_generator():
    criteria = read_yaml_file(paths.DEPENDANCIES_CRITERIA_FPATH)
    for category in criteria.keys():
        for sub_category in criteria[category].keys():
            for criterion_id in criteria[category][sub_category].keys():
                yield criterion_id, criteria[category][sub_category][criterion_id]


def license_criterion_generator():
    criteria = read_yaml_file(paths.LICENSE_CRITERIA_FPATH)
    for category in criteria.keys():
        for sub_category in criteria[category].keys():
            for criterion_id in criteria[category][sub_category].keys():
                yield criterion_id, criteria[category][sub_category][criterion_id]


def structure_criterion_generator():
    criteria = read_yaml_file(paths.STRUCTURE_CRITERIA_FPATH)
    for category in criteria.keys():
        for sub_category in criteria[category].keys():
            for criterion_id in criteria[category][sub_category].keys():
                yield criterion_id, criteria[category][sub_category][criterion_id]
