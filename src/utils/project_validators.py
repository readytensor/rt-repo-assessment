import os
from typing import Dict, List
from fnmatch import fnmatch
from utils import IGNORED_PATTERNS, SCRIPT_EXTENSIONS


def has_readme(directory_path: str) -> bool:
    """
    Check if a repository has a README.md file.

    Args:
        directory_path (str): Path to the repository root

    Returns:
        bool: True if README.md exists, False otherwise
    """
    readme_path = os.path.join(directory_path, "README.md")
    print(readme_path)
    return os.path.exists(readme_path)


def has_requirements_txt(directory_path: str) -> bool:
    """
    Check if a repository has a requirements.txt file.

    Args:
        directory_path (str): Path to the repository root

    Returns:
        bool: True if requirements.txt exists, False otherwise
    """
    requirements_path = os.path.join(directory_path, "requirements.txt")
    return os.path.exists(requirements_path)


def has_pyproject_toml(directory_path: str) -> bool:
    """
    Check if a repository has a pyproject.toml file.

    Args:
        directory_path (str): Path to the repository root

    Returns:
        bool: True if pyproject.toml exists, False otherwise
    """
    pyproject_path = os.path.join(directory_path, "pyproject.toml")
    return os.path.exists(pyproject_path)


def has_setup_py(directory_path: str) -> bool:
    """
    Check if a repository has a setup.py file.
    """
    setup_path = os.path.join(directory_path, "setup.py")
    return os.path.exists(setup_path)


def has_license_file(directory_path: str) -> bool:
    """
    Check if a repository has a LICENSE file.

    Args:
        directory_path (str): Path to the repository root

    Returns:
        bool: True if LICENSE file exists, False otherwise
    """
    license_path = os.path.join(directory_path, "LICENSE")
    return os.path.exists(license_path)


def has_gitignore_file(directory_path: str) -> bool:
    """
    Check if a repository has a .gitignore file.

    Args:
        directory_path (str): Path to the repository root

    Returns:
        bool: True if .gitignore file exists, False otherwise
    """
    gitignore_path = os.path.join(directory_path, ".gitignore")
    return os.path.exists(gitignore_path)


def has_ignored_files(directory_path: str) -> List[str]:
    """
    Check if a repository has ignored files.

    Args:
        directory_path (str): Path to the repository root

    Returns:
        List[str]: List of ignored files
    """
    found_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file in IGNORED_PATTERNS:
                found_files.append(os.path.join(root, file))
    return found_files


def has_descriptive_title(directory_path: str) -> bool:
    """
    Check if the readme has a descriptive title.

    Args:
        directory_path (str): Path to the repository root

    Returns:
        bool: True if the readme has a descriptive title, False otherwise
    """
    readme_path = os.path.join(directory_path, "README.md")
    if not os.path.exists(readme_path):
        return False
    with open(readme_path, "r") as f:
        content = f.read()

    return content.startswith("#") or content.startswith("##")


def get_directory_depth(
    directory_path: str, ignored_patterns: List[str] = IGNORED_PATTERNS
) -> int:
    """
    Calculate the depth of the directory structure of a repository.

    Args:
        directory_path (str): Path to the repository root
        ignored_patterns (List[str]): List of patterns to ignore

    Returns:
        int: Depth of the directory structure
    """
    max_depth = 0
    base_depth = len(directory_path.rstrip(os.sep).split(os.sep))

    for dirpath, dirnames, files in os.walk(directory_path, topdown=True):
        # Modify dirnames in-place to prevent os.walk from recursing into ignored directories

        dirnames[:] = [
            d for d in dirnames if not any(fnmatch(d, pat) for pat in ignored_patterns)
        ]

        # Skip files that match ignored patterns
        files = [
            f for f in files if not any(fnmatch(f, pat) for pat in ignored_patterns)
        ]

        if files:
            current_depth = len(dirpath.rstrip(os.sep).split(os.sep)) - base_depth
            max_depth = max(max_depth, current_depth)

    return max_depth


def get_script_lengths(directory_path: str) -> Dict[str, int]:
    """
    Get the lengths of all scripts in a repository.
    """
    script_lengths = {}
    for root, _, files in os.walk(directory_path):
        for file in files:
            if any(file.endswith(ext) for ext in SCRIPT_EXTENSIONS):
                with open(
                    os.path.join(root, file), "r", encoding="utf-8", errors="ignore"
                ) as f:
                    script_lengths[file] = len(f.readlines())
    return script_lengths
