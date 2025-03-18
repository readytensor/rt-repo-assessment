import os
import subprocess
import zipfile
import shutil
import requests
from fnmatch import fnmatch
from typing import Optional, List
from logger import get_logger

logger = get_logger(__name__)


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
            logger.info(f"Repository already exists in {output_dir}, removing it")
            shutil.rmtree(output_dir)

        # Create target directory
        os.makedirs(output_dir, exist_ok=True)

        # Convert repo URL to zip download URL
        if repo_url.endswith(".git"):
            repo_url = repo_url[:-4]
        if repo_url.endswith("/"):
            repo_url = repo_url[:-1]

        # Extract repo name from URL
        repo_name = os.path.basename(repo_url)
        download_url = f"{repo_url}/archive/refs/heads/main.zip"

        # Download and extract the repository
        logger.info(f"Downloading repository from {download_url}")
        import requests

        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        # Create a temporary directory for initial extraction
        temp_dir = os.path.join(output_dir, "_temp_extract")
        os.makedirs(temp_dir, exist_ok=True)

        temp_zip = os.path.join(temp_dir, "repo.zip")
        with open(temp_zip, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Extract the downloaded zip to the temporary directory
        with zipfile.ZipFile(temp_zip, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        # Find the nested directory (it's usually named 'repo-name-main')
        nested_dirs = [
            d for d in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, d))
        ]
        if nested_dirs:
            nested_dir = os.path.join(temp_dir, nested_dirs[0])

            # Move all contents from the nested directory to the output directory
            for item in os.listdir(nested_dir):
                source = os.path.join(nested_dir, item)
                destination = os.path.join(output_dir, item)
                if os.path.isdir(source):
                    shutil.copytree(source, destination)
                else:
                    shutil.copy2(source, destination)

        # Clean up temporary files
        shutil.rmtree(temp_dir)

        # Extract additional zip file if provided
        if zip_path:
            if not os.path.exists(zip_path):
                logger.error(f"Zip file not found: {zip_path}")
                return False

            logger.info(f"Extracting additional zip file: {zip_path}")
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(output_dir)

        return True

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download repository: {str(e)}")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        return False

    except zipfile.BadZipFile as e:
        logger.error(f"Invalid zip file: {str(e)}")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        return False

    except OSError as e:
        logger.error(f"OS error occurred: {str(e)}")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        return False

    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        return False


def is_repo_public(repo_url: str) -> bool:
    """
    Check if a GitHub repository is public.

    Args:
        repo_url (str): URL of the GitHub repository to check

    Returns:
        bool: True if the repository is public, False otherwise
    """
    try:
        # Clean up the URL to get the API endpoint
        if repo_url.endswith(".git"):
            repo_url = repo_url[:-4]
        if repo_url.endswith("/"):
            repo_url = repo_url[:-1]

        # Extract owner and repo name from URL
        # Example: https://github.com/owner/repo
        parts = repo_url.split("/")
        if "github.com" in parts:
            github_index = parts.index("github.com")
            if len(parts) >= github_index + 3:
                owner = parts[github_index + 1]
                repo = parts[github_index + 2]

                # Use GitHub API to check repo visibility
                api_url = f"https://api.github.com/repos/{owner}/{repo}"
                response = requests.get(api_url)

                if response.status_code == 200:
                    repo_data = response.json()
                    return not repo_data.get("private", True)
                else:
                    # If we get a 404, the repo doesn't exist or is private
                    return False

        # For non-GitHub URLs or malformed URLs, try to access the repo directly
        response = requests.head(repo_url)
        return response.status_code == 200

    except Exception as e:
        logger.error(f"Error checking repository visibility: {str(e)}")
        return False


def clone_repo(repo_url: str, output_dir: str, branch: str = "main") -> bool:
    """
    Clone a git repository using git command.

    Args:
        repo_url (str): URL of the git repository to clone
        output_dir (str): Directory where to clone the repository
        branch (str, optional): Branch to clone, defaults to 'main'

    Returns:
        bool: True if successful, False otherwise

    Raises:
        OSError: If there are file system related errors
    """
    try:
        if os.path.exists(output_dir):
            logger.info(f"Repository already exists in {output_dir}, removing it")
            shutil.rmtree(output_dir)

        # Create parent directory if it doesn't exist
        parent_dir = os.path.dirname(output_dir)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        # Clone the repository
        logger.info(f"Cloning repository from {repo_url} to {output_dir}")

        # Use git clone command with specified branch
        result = subprocess.run(
            ["git", "clone", "--branch", branch, repo_url, output_dir],
            check=True,
            capture_output=True,
            text=True,
        )

        logger.info(f"Successfully cloned repository: {result.stdout}")
        return True

    except subprocess.CalledProcessError as e:
        logger.error(f"Git clone failed: {e.stderr}")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        return False

    except OSError as e:
        logger.error(f"OS error occurred: {str(e)}")
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        return False

    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
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
            logger.warning(f"No README.md or readme.md found in {repo_path}")
            return None

    ## Try multiple encodings
    encodings_to_try = ["utf-8", "ISO-8859-1", "cp1252"]

    for encoding in encodings_to_try:
        try:
            with open(readme_path, "r", encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            logger.warning(
                f"Error decoding the file with {encoding} encoding. Trying next encoding."
            )

    # If all encodings fail, return None
    logger.error(
        f"Failed to decode the file with available encodings: {encodings_to_try}"
    )
    return None


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
        logger.error(f"Error generating repository tree: {str(e)}")
        return ""
