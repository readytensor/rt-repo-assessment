from config import paths
from utils.general import read_yaml_file

TRACKED_FILES = read_yaml_file(paths.TRACKED_FILES_FPATH)

IGNORED_PATTERNS = TRACKED_FILES["ignored_names"]

SCRIPT_EXTENSIONS = TRACKED_FILES["script_extensions"]


__all__ = ["IGNORED_PATTERNS", "SCRIPT_EXTENSIONS"]
