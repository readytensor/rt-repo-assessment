import os
import zipfile
import shutil
from git import Repo
from git.exc import GitCommandError
from fnmatch import fnmatch
from typing import Optional, List


def download_and_extract_repo(
    repo_url: str, output_dir: str, zip_path: Optional[str] = None
) -> bool:
    """
    Download a git repository and extract it.

    Args:
        repo_url (str): URL of the git repository to download
        output_dir (str): Directory where to extract the repository
        zip_path (str, optional): Path to zip file to extract after downloading

    Returns:
        bool: True if successful, False otherwise

    Raises:
        OSError: If there are file system related errors
    """

    try:
        if os.path.exists(output_dir):
            print(f"Repository already exists in {output_dir}, removing it")
            shutil.rmtree(output_dir)

        # Create target directory
        os.makedirs(output_dir, exist_ok=True)

        # Convert repo URL to zip download URL
        if repo_url.endswith(".git"):
            repo_url = repo_url[:-4]
        if repo_url.endswith("/"):
            repo_url = repo_url[:-1]
        download_url = f"{repo_url}/archive/refs/heads/main.zip"

        # Download and extract the repository
        print(f"Downloading repository from {download_url}")
        import requests

        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        temp_zip = os.path.join(output_dir, "repo.zip")
        with open(temp_zip, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Extract the downloaded zip
        with zipfile.ZipFile(temp_zip, "r") as zip_ref:
            zip_ref.extractall(output_dir)

        # Remove the temporary zip file
        os.remove(temp_zip)

        # Extract additional zip file if provided
        if zip_path:
            if not os.path.exists(zip_path):
                print(f"Zip file not found: {zip_path}")
                return False

            print(f"Extracting additional zip file: {zip_path}")
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(output_dir)

        return True

    except requests.exceptions.RequestException as e:
        print(f"Failed to download repository: {str(e)}")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        return False

    except zipfile.BadZipFile as e:
        print(f"Invalid zip file: {str(e)}")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        return False

    except OSError as e:
        print(f"OS error occurred: {str(e)}")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        return False

    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        return False


def get_readme_content(repo_path: str) -> Optional[str]:
    # Try README.md first
    readme_path = os.path.join(repo_path, "README.md")
    if not os.path.exists(readme_path):
        # Try readme.md if README.md not found
        readme_path = os.path.join(repo_path, "readme.md")
        if not os.path.exists(readme_path):
            print(f"No README.md or readme.md found in {repo_path}")
            return None

    with open(readme_path, "r") as file:
        return file.read()


def get_repo_tree(repo_path: str, ignore_patterns: Optional[List[str]] = None) -> str:
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
        print(f"Error generating repository tree: {str(e)}")
        return ""
