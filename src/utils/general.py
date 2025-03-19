import os
import json
import yaml
from typing import Dict, List, Union, Any


def read_yaml_file(file_path: str) -> Dict[Any, Any]:
    """Read a YAML file and return its content."""
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def write_yaml_file(file_path: str, data: Union[Dict, List]):
    """Write data to a YAML file with nice formatting.

    Args:
        file_path: Path to the output YAML file
        data: Dictionary or list to be written to YAML
    """
    with open(file_path, "w") as file:
        yaml.dump(
            data,
            file,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
            allow_unicode=True,
        )


def read_json_file(file_path: str) -> Union[Dict, List]:
    """Read a JSON file and return its content."""
    with open(file_path, "r") as file:
        return json.load(file)


def write_json_file(file_path: str, data: Union[Dict, List]):
    """Write data to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_dir_size_mb(directory):
    """Get the total size of a directory in megabytes."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # Skip if it's a symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    # Convert bytes to megabytes
    size_in_mb = total_size / (1024 * 1024)
    return size_in_mb
