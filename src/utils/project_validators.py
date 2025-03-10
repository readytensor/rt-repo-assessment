import os
from typing import List
from fnmatch import fnmatch
from utils import IGNORED_PATTERNS


def has_readme(repo_path: str) -> bool:
    """
    Check if a repository has a README.md file.

    Args:
        repo_path (str): Path to the repository root

    Returns:
        bool: True if README.md exists, False otherwise
    """
    readme_path = os.path.join(repo_path, "README.md")
    return os.path.exists(readme_path)


def has_requirements_txt(repo_path: str) -> bool:
    """
    Check if a repository has a requirements.txt file.

    Args:
        repo_path (str): Path to the repository root

    Returns:
        bool: True if requirements.txt exists, False otherwise
    """
    requirements_path = os.path.join(repo_path, "requirements.txt")
    return os.path.exists(requirements_path)


def has_pyproject_toml(repo_path: str) -> bool:
    """
    Check if a repository has a pyproject.toml file.

    Args:
        repo_path (str): Path to the repository root

    Returns:
        bool: True if pyproject.toml exists, False otherwise
    """
    pyproject_path = os.path.join(repo_path, "pyproject.toml")
    return os.path.exists(pyproject_path)


def has_setup_py(repo_path: str) -> bool:
    """
    Check if a repository has a setup.py file.
    """
    setup_path = os.path.join(repo_path, "setup.py")
    return os.path.exists(setup_path)


def has_license_file(repo_path: str) -> bool:
    """
    Check if a repository has a LICENSE file.

    Args:
        repo_path (str): Path to the repository root

    Returns:
        bool: True if LICENSE file exists, False otherwise
    """
    license_path = os.path.join(repo_path, "LICENSE")
    return os.path.exists(license_path)


def has_gitignore_file(repo_path: str) -> bool:
    """
    Check if a repository has a .gitignore file.

    Args:
        repo_path (str): Path to the repository root

    Returns:
        bool: True if .gitignore file exists, False otherwise
    """
    gitignore_path = os.path.join(repo_path, ".gitignore")
    return os.path.exists(gitignore_path)


def has_ignored_files(repo_path: str) -> List[str]:
    """
    Check if a repository has ignored files.

    Args:
        repo_path (str): Path to the repository root

    Returns:
        List[str]: List of ignored files
    """
    found_files = []
    ignored_files = [
        ".git",
        ".DS_Store",
        "__pycache__",
        ".pytest_cache",
        "*.pyc",
        ".venv",
        "venv",
    ]
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file in ignored_files:
                found_files.append(os.path.join(root, file))
    return found_files


def has_descriptive_title(repo_path: str) -> bool:
    """
    Check if the readme has a descriptive title.

    Args:
        repo_path (str): Path to the repository root

    Returns:
        bool: True if the readme has a descriptive title, False otherwise
    """
    readme_path = os.path.join(repo_path, "README.md")
    if not os.path.exists(readme_path):
        return False
    with open(readme_path, "r") as f:
        content = f.read()

    return content.startswith("#") or content.startswith("##")


def get_directory_depth(
    repo_path: str, ignored_patterns: List[str] = IGNORED_PATTERNS
) -> int:
    """
    Calculate the depth of the directory structure of a repository.

    Args:
        repo_path (str): Path to the repository root
        ignored_patterns (List[str]): List of patterns to ignore

    Returns:
        int: Depth of the directory structure
    """
    max_depth = 0
    base_depth = len(repo_path.rstrip(os.sep).split(os.sep))

    for dirpath, dirnames, files in os.walk(repo_path, topdown=True):
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
