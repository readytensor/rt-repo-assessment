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
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
