import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SRC_DIR = os.path.join(ROOT_DIR, "src")

DATA_DIR = os.path.join(ROOT_DIR, "data")

INPUTS_DIR = os.path.join(DATA_DIR, "inputs")

OUTPUTS_DIR = os.path.join(DATA_DIR, "outputs")

CONFIG_DIR = os.path.join(SRC_DIR, "config")

SCORING_DIR = os.path.join(CONFIG_DIR, "scoring")

SCORING_CRITERIA_FPATH = os.path.join(SCORING_DIR, "scoring_criteria.yaml")
