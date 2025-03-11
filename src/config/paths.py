import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SRC_DIR = os.path.join(ROOT_DIR, "src")

DATA_DIR = os.path.join(ROOT_DIR, "data")

INPUTS_DIR = os.path.join(DATA_DIR, "inputs")

OUTPUTS_DIR = os.path.join(DATA_DIR, "outputs")

CONFIG_DIR = os.path.join(SRC_DIR, "config")

CONFIG_FPATH = os.path.join(CONFIG_DIR, "config.json")

SCORING_DIR = os.path.join(CONFIG_DIR, "scoring")

PROMPTS_FPATH = os.path.join(CONFIG_DIR, "prompts.yaml")

CODE_QUALITY_CRITERIA_FPATH = os.path.join(SCORING_DIR, "code_quality_criteria.yaml")

DEPENDANCIES_CRITERIA_FPATH = os.path.join(SCORING_DIR, "dependancies_criteria.yaml")

LICENSE_CRITERIA_FPATH = os.path.join(SCORING_DIR, "license_criteria.yaml")

STRUCTURE_CRITERIA_FPATH = os.path.join(SCORING_DIR, "structure_criteria.yaml")

DOCUMENTATION_CRITERIA_FPATH = os.path.join(SCORING_DIR, "documentation_criteria.yaml")

TRACKED_FILES_FPATH = os.path.join(CONFIG_DIR, "tracked_files.yaml")
