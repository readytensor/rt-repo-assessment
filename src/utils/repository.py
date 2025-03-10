import os
import zipfile
import shutil
import logging
from git import Repo
from git.exc import GitCommandError
from fnmatch import fnmatch


def clone_and_extract_repo(
    repo_url: str, output_dir: str, zip_path: str = None
) -> bool:
    """
    Clone a git repository and optionally extract a zip file.

    Args:
        repo_url (str): URL of the git repository to clone
        output_dir (str): Directory where to clone the repository
        zip_path (str, optional): Path to zip file to extract after cloning

    Returns:
        bool: True if successful, False otherwise

    Raises:
        GitCommandError: If there's an error cloning the repository
        zipfile.BadZipFile: If the zip file is corrupted
        OSError: If there are file system related errors
    """

    if os.path.exists(output_dir):
        logging.info(f"Repository already cloned in {output_dir}")
        return True

    try:
        # Create target directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Clone the repository
        logging.info(f"Cloning repository from {repo_url} to {output_dir}")

        # Clone the repository
        Repo.clone_from(repo_url, output_dir)

        # Extract zip file if provided
        if zip_path:
            if not os.path.exists(zip_path):
                logging.error(f"Zip file not found: {zip_path}")
                return False

            logging.info(f"Extracting zip file: {zip_path}")
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(output_dir)

        return True

    except GitCommandError as e:
        logging.error(f"Git clone failed: {str(e)}")
        # Clean up target directory if it exists
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        return False

    except zipfile.BadZipFile as e:
        logging.error(f"Invalid zip file: {str(e)}")
        return False

    except OSError as e:
        logging.error(f"OS error occurred: {str(e)}")
        return False

    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        return False


def get_readme_content(repo_path: str) -> str:
    # Try README.md first
    readme_path = os.path.join(repo_path, "README.md")
    if not os.path.exists(readme_path):
        # Try readme.md if README.md not found
        readme_path = os.path.join(repo_path, "readme.md")
        if not os.path.exists(readme_path):
            logging.error(f"No README.md or readme.md found in {repo_path}")
            return None

    with open(readme_path, "r") as file:
        return file.read()


def get_repo_tree(repo_path: str, ignore_patterns: list = None) -> str:
    """
    Generate a tree-like string representation of the repository structure.

    Args:
        repo_path (str): Path to the repository root
        ignore_patterns (list, optional): List of patterns to ignore (e.g., ['.git', '__pycache__'])

    Returns:
        str: String representation of the repository tree structure
    """
    if ignore_patterns is None:
        ignore_patterns = [".git", "__pycache__", ".pytest_cache", "*.pyc", ".DS_Store"]

    def should_ignore(path):
        name = os.path.basename(path)
        return any(fnmatch(name, pattern) for pattern in ignore_patterns)

    def generate_tree(dir_path: str, prefix: str = "") -> str:
        if not os.path.exists(dir_path):
            return "Directory not found"

        output = []
        entries = os.listdir(dir_path)
        entries.sort()

        # Filter out ignored patterns
        entries = [e for e in entries if not should_ignore(os.path.join(dir_path, e))]

        for i, entry in enumerate(entries):
            path = os.path.join(dir_path, entry)
            is_last = i == len(entries) - 1

            # Create the appropriate prefix for the current item
            current_prefix = "└── " if is_last else "├── "

            # Add the current entry to the output
            output.append(prefix + current_prefix + entry)

            # If it's a directory, recursively process its contents
            if os.path.isdir(path):
                # Extend prefix for nested items
                extension = "    " if is_last else "│   "
                output.append(generate_tree(path, prefix + extension))

        return "\n".join(filter(None, output))

    try:
        tree_structure = generate_tree(repo_path)
        return f"{os.path.basename(repo_path)}\n{tree_structure}"
    except Exception as e:
        logging.error(f"Error generating repository tree: {str(e)}")
        return None
