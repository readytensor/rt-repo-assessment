# GitHub Repository Assessment

## Overview

This project implements an **AI-driven assessment framework** to analyze GitHub repositories using **Large Language Models (LLMs)** and **rule-based techniques**. It evaluates key software quality dimensions to ensure adherence to **best practices** and industry standards.

### Core Evaluation Categories

Each repository is assessed across five **critical dimensions** to guarantee excellence:

- **Documentation** – Comprehensive, well-structured, and user-centric guidance for seamless adoption.
- **Repository Structure** – Intuitive, standardized organization that enhances collaboration and scalability.
- **Environment & Dependencies** – Robust dependency management ensuring reproducibility and seamless execution.
- **License & Legal** – Clear governance of intellectual property, permissions, and compliance.
- **Code Quality** – Enforced coding standards ensuring efficiency, maintainability, and technical integrity.

This framework structured into three progressive tiers:

- **Essential** – Establishes foundational repository standards and ensures minimal compliance.
- **Professional** – Implements structured, maintainable, and scalable repository practices.
- **Elite** – Adopts best-in-class methodologies, including advanced documentation, automation, and security enforcement.

## Built With

This project is powered by:

- **Python (>=3.12)** – Core language.
- **LangChain (>=0.3.20)** – LLM-driven framework.

For full dependencies, see [`pyproject.toml`](./pyproject.toml).

## Target Audience

- **Primary Focus**: AI/ML and data science projects.
- **Broader Applicability**: The principles of good documentation, organization, and reproducibility are beneficial for all software repositories.

## Getting Started

### Prerequisites

- Python 3.12 or higher
- `uv` package for package management

### Installation Guide

#### Package & Project Management with `uv`

This project leverages `uv` ([official documentation](https://docs.astral.sh/uv)) for efficient package and dependency management, ensuring seamless setup and environment consistency.

1. **Clone the Repository**Begin by cloning the repository to your local environment:

   ```bash
   git clone https://github.com/readytensor/rt-repo-assessment.git
   cd rt-repo-assessment
   ```
2. **Install `uv`**Run the following command to install `uv`:

   ```bash
   pip install uv
   ```

   [How to install uv](https://docs.astral.sh/uv/getting-started/installation/)
3. **Install Python & Dependencies**
   Set up Python and install all dependencies in a virtual environment using:

   ```bash
   make install
   ```
4. **Adding New Packages**
   To add a package to the project, use the following command:

   ```bash
   uv add <package>
   ```

## Usage

1. **Run the Assessment**
   Execute the repository assessment tool using:
   ```bash
   python main.py 
   ```
2. **Configure Repository URLs & Max Workers**
   Configurations are specified in `/src/config/config.json`
   Modify config.json to specify repository URLs:
   ```bash
   {
   "urls": [
       "https://github.com/repo_name"
   ],
   "max_workers": 12
   }
   ```
3. **View Assessment Results**
   The assessment results can be found in the `data/outputs/repo_name/report.md` file.

**Overall Summary**

- **Total Criteria**: Total Number of Criteria
- **Criteria Met**: Percentage of Criteria Met

 **Category Breakdown**

| Category     | Criteria Met                | Total Criteria              | Percentage |
| ------------ | --------------------------- | --------------------------- | ---------- |
| Essential    | # Essential Criteria Met    | Total Essential Criteria    | %          |
| Professional | # Professional Criteria Met | Total Professional Criteria | %          |
| Elite        | # Elite Criteria Met        | Total Elite Criteria        | %          |

 **Sample Detailed Results**

| Category                   | Criterion                 | Status | Explanation                                                                                                                                                                                                                          |
| -------------------------- | ------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Code Quality               | Modular Code Organization | ✅     | This criterion is satisfied in the project by file 'utils.py'. The code is organized into functions and a class, which is a good practice.                                                                                           |
| Documentation              | README Completeness       | ✅     | The README provides all necessary information for understanding, setting up, and using the project effectively.                                                                                                                      |
| Repository Structure       | Clear Folder Organization | ✅     | The repository follows a logical structure with clear divisions for source code, documentation, and other assets.                                                                                                                    |
| Environment & Dependencies | Test Directory Structure  | ❌     | The project directory does not contain a dedicated 'tests/' directory or any other structure that organizes tests in a way that mirrors the main code structure. There is no indication of any testing files or directories present. |
| License and Legal          | License Presence          | ✅     | The project directory includes a recognized license file named 'LICENSE.txt' in the root directory, which explicitly states the terms of use, modification, and distribution.                                                        |

---

## Data Requirements

### Expected Data Sources and Setup

This project analyzes GitHub repositories by fetching data from the provided repository links. The expected data sources include:

- **GitHub Repository Links**: A list of GitHub repository URLs that the framework will analyze.

The evaluation data consists of:

- **README Files**: To evaluate documentation quality.
- **Repository Metadata**: To assess repository structure, dependencies, and license information.
- **Code Files**: For evaluating code quality and enforcing coding standards.

Ensure your GitHub repositories are public, or that you have the necessary access rights for private repositories. The project will automatically fetch the data from these repositories when provided with their URLs.

For example:

```json
{
  "repository_urls": [
    "https://github.com/readytensor/rt-repo-assessment",
    "https://github.com/another-user/sample-repo"
  ]
}
```

## Testing

The project uses `pytest` for unit testing. Tests can be run using the `make test` command.

## Configuration

The configuration is managed through the `config.json` and scoring files.

As detailed in the usage section, the config.json defines key parameters like repository URLs and the maximum number of concurrent workers.

### Scoring Criteria

Scoring is based on five key areas: Documentation, Repository Structure, Environment & Dependencies, License & Legal, and Code Quality. Each criterion is assessed at three levels: **Essential**, **Professional**, and **Elite**.

The assessment framework employs three types of scoring methods:

1. **Logic-based Scoring**: Relies on predefined functions that apply specific validation rules and tests.
2. **File Content-based Scoring**: Uses LLMs to evaluate the content of files against defined criteria.
3. **Metadata-based Scoring**: Uses LLMs on repository metadata such as directory structure and file presence.

#### Examples of Different Scoring Types:

##### Logic-based Scoring Example

```yaml
script_length:
  name: Script Length Control
  description: Individual scripts/modules have reasonable length (< 500 lines)
  essential: true
  professional: true
  elite: true
  based_on: custom_logic
  args:
    max_script_length: 500
```

Logic-based scoring uses custom functions to validate criteria such as script length against configurable thresholds.

##### Custom Logic Function Example

Here's how a custom logic function processes the metadata to evaluate a criterion:

```python
@scoring_function
def script_length(metadata: Dict[str, Any], max_script_length: int) -> Dict[str, Any]:
    """
    Check if scripts in the repository exceed the maximum allowed length.
    """
    script_lengths = metadata["script_lengths"]
    long_scripts = []
    score = 1
    explanation = "All scripts are less than 500 lines."
    
    for script, length in script_lengths.items():
        if length > max_script_length:
            score = 0
            long_scripts.append(script)
            explanation = f"The following scripts are longer than {max_script_length} lines: {long_scripts}"

    return {
        "score": score,
        "explanation": explanation,
    }
```

This function analyzes the script lengths in the metadata and assigns a score of 1 if all scripts meet the length requirement, or 0 if any scripts exceed it.

##### File Content-based Scoring Example

```yaml
functions_and_classes:
  name: Modular Code Organization
  description: Code organized into functions/methods rather than monolithic scripts
  essential: true
  professional: true
  elite: true
  include_extensions:
  - .py
  - .ipynb
  aggregation: OR
  based_on: file_content
```

File content-based scoring examines the actual content of code files, checking for proper modularization and organization.

##### Metadata-based Scoring Example

```yaml
organized_notebooks:
  name: Organized Notebooks
  description: If Jupyter notebooks are present, they are organized in a logical manner
  essential: false
  professional: true
  elite: true
  instructions: If the repository does not contain any notebooks, this criterion should be scored 1.
```

Metadata-based scoring evaluates repository structure and organization patterns rather than specific file contents.

##### Repository Metadata Structure

The assessment framework extracts repository metadata, which is then used for evaluation:

```python
# Example of repository metadata structure
metadata = {
    # File existence checks
    "readme_exists": True,
    "requirements_txt_exists": True, 
    "pyproject_toml_exists": False,
    "setup_py_exists": True,
    "license_file_exists": True,
    "gitignore_file_exists": True,
    "ignored_files_exist": True,
    
    # Script length information
    "script_lengths": {
        "src/main.py": 178,
        "src/utils/repository.py": 309,
        "src/utils/project_validators.py": 171
    },
    
    # Repository directory structure as a formatted string
    "directory_structure": 
        repo_name
        ├── src
        │   ├── utils
        │   │   ├── repository.py
        │   │   └── project_validators.py
        │   └── main.py
        ├── README.md
        ├── LICENSE
        └── requirements.txt   
}
```

This metadata provides a comprehensive overview of the repository structure and key characteristics, enabling both rule-based and LLM-based evaluation against the defined criteria.

## Contributing

We welcome contributions to improve the framework. Please refer to the guidelines below for how you can contribute:

1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request with a detailed description of your modifications.

## License

This project is licensed under the [MIT License](https://github.com/readytensor/rt-repo-assessment/blob/main/LICENSE).

## Citation

- **Ready Tensor, Inc. (2025).**  [Best Practices for AI Project Code Repositories.](https://app.readytensor.ai/publications/best-practices-for-ai-project-code-repositories-0llldKKtn8Xb)

## Contact

For any inquiries, feel free to reach out to support@readytensor.com

