import os
import pytest
import tempfile
import shutil
from src.utils.project_validators import (
    has_readme,
    has_requirements_txt,
    has_setup_py,
    has_license_file,
    has_gitignore_file,
)


@pytest.fixture
def temp_repo_dir():
    """Create a temporary directory for testing repository validators"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup after test
    shutil.rmtree(temp_dir)


def test_has_readme(temp_repo_dir):
    """Test detection of README.md file"""
    # Initially should return False
    assert not has_readme(temp_repo_dir)

    # Create a README.md file
    with open(os.path.join(temp_repo_dir, "README.md"), "w") as f:
        f.write("# Test Repository")

    # Now should return True
    assert has_readme(temp_repo_dir)


def test_has_requirements_txt(temp_repo_dir):
    """Test detection of requirements.txt file"""
    # Initially should return False
    assert not has_requirements_txt(temp_repo_dir)

    # Create a requirements.txt file
    with open(os.path.join(temp_repo_dir, "requirements.txt"), "w") as f:
        f.write("numpy==1.21.0\npandas==1.3.0")

    # Now should return True
    assert has_requirements_txt(temp_repo_dir)


def test_has_setup_py(temp_repo_dir):
    """Test detection of setup.py file"""
    # Initially should return False
    assert not has_setup_py(temp_repo_dir)

    # Create a setup.py file
    with open(os.path.join(temp_repo_dir, "setup.py"), "w") as f:
        f.write("from setuptools import setup")

    # Now should return True
    assert has_setup_py(temp_repo_dir)


def test_has_license_file(temp_repo_dir):
    """Test detection of LICENSE file"""
    # Initially should return False
    assert not has_license_file(temp_repo_dir)

    # Create a LICENSE file
    with open(os.path.join(temp_repo_dir, "LICENSE"), "w") as f:
        f.write("MIT License")

    # Now should return True
    assert has_license_file(temp_repo_dir)


def test_has_gitignore_file(temp_repo_dir):
    """Test detection of .gitignore file"""
    # Initially should return False
    assert not has_gitignore_file(temp_repo_dir)

    # Create a .gitignore file
    with open(os.path.join(temp_repo_dir, ".gitignore"), "w") as f:
        f.write("__pycache__/\n*.py[cod]")

    # Now should return True
    assert has_gitignore_file(temp_repo_dir)


def test_multiple_validators(temp_repo_dir):
    """Test multiple validators together"""
    # Create all files
    with open(os.path.join(temp_repo_dir, "README.md"), "w") as f:
        f.write("# Test Repository")

    with open(os.path.join(temp_repo_dir, "requirements.txt"), "w") as f:
        f.write("numpy==1.21.0\npandas==1.3.0")

    with open(os.path.join(temp_repo_dir, "setup.py"), "w") as f:
        f.write("from setuptools import setup")

    with open(os.path.join(temp_repo_dir, "LICENSE"), "w") as f:
        f.write("MIT License")

    with open(os.path.join(temp_repo_dir, ".gitignore"), "w") as f:
        f.write("__pycache__/\n*.py[cod]")

    # All validators should return True
    assert has_readme(temp_repo_dir)
    assert has_requirements_txt(temp_repo_dir)
    assert has_setup_py(temp_repo_dir)
    assert has_license_file(temp_repo_dir)
    assert has_gitignore_file(temp_repo_dir)
