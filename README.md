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
This project is powered by the following technologies:

- **Python (>=3.12)** - The core language for this project.
- **GitPython (>=3.1.44)** - For Git repository interactions.
- **Langchain (>=0.3.20)** - Framework for LLM-powered assessments.
- **Langchain-Community (>=0.3.19)** - Community-driven extensions to Langchain.
- **Langchain-OpenAI (>=0.3.8)** - OpenAI integration for advanced LLM tasks.
- **Pandas (>=2.2.3)** - Data manipulation and analysis.
- **python-dotenv (>=1.0.1)** - Manages environment variables.
- **PyYAML (>=6.0.2)** - Handles YAML files for configuration.
- **Mypy (>=1.15.0)** - Static type checker for Python.

## Getting Started
### Prerequisites
- Python 3.12 or higher
- `uv` package for package management

### Installation Guide

#### Package & Project Management with `uv`
This project leverages `uv` ([official documentation](https://docs.astral.sh/uv)) for efficient package and dependency management, ensuring seamless setup and environment consistency.

1. **Clone the Repository**  
   Begin by cloning the repository to your local environment:
   ```bash
   git clone https://github.com/readytensor/rt-repo-assessment.git
   cd rt-repo-assessment
   ```
2. **Install `uv`**  
   Run the following command to install `uv`:
   ```bash
   pip install uv
   ```

   [How to install uv](https://docs.astral.sh/uv/getting-started/installation/)

3. **Install Python & Dependencies**
   Set up Python and install all dependencies in a virtual environment using:  
   ```bash
   make install
   ```

4 . **Adding New Packages**  
   To add a package to the project, use the following command:
   ```bash
   uv add <package>
   ```

## Usage  

1.**Run the Assessment** 
    Execute the repository assessment tool using:  
    ```bash
    python main.py 
    ```
2.**Configure Repository URLs & Max Workers**
    Modify config.json to specify repository URLs:
    ```bash
    {
    "urls": [
        "https://github.com/repo_name"
    ],
    "max_workers": 12
    }
    ```
3.**View Assessment Results**
    The assessment results can be found in the `Output/Repo name/report.md` file.

### Overall Summary

- **Total Criteria**: [Total Number of Criteria]
- **Criteria Met**: [Percentage of Criteria Met]

### Category Breakdown

| Category      | Criteria Met | Total Criteria | Percentage   |
|---------------|--------------|----------------|--------------|
| Essential     | [Criteria Met for Essential] | [Total Criteria for Essential] | % |
| Professional  | [Criteria Met for Professional] | [Total Criteria for Professional] | % |
| Elite         | [Criteria Met for Elite] | [Total Criteria for Elite] | % |


### Detailed Results

| Category            | Criterion                         | Status | Explanation |
|---------------------|-----------------------------------|--------|-------------|
| **Code Quality**     | Modular Code Organization         | ✅     | This criterion is satisfied in the project by file 'utils.py'. The code is organized into functions and a class, which is a good practice. |. |
| **Documentation**    | README Completeness               | ✅     | The README provides all necessary information for understanding, setting up, and using the project effectively. |
| **Repository Structure** | Clear Folder Organization     | ✅     | The repository follows a logical structure with clear divisions for source code, documentation, and other assets. |
| **Environment & Dependencies** |Test Directory Structure | ❌   | The project directory does not contain a dedicated 'tests/' directory or any other structure that organizes tests in a way that mirrors the main code structure. There is no indication of any testing files or directories present. | |
| License and Legal     | License Presence                  | ✅ | The project directory includes a recognized license file named 'LICENSE.txt' in the root directory, which explicitly states the terms of use, modification, and distribution. |

---
## Target Audience

- **Primary Focus**: AI/ML and data science projects.
- **Broader Applicability**: The principles of good documentation, organization, and reproducibility are beneficial for all software repositories.

## Maintenance Status

- **Current Status**: Actively maintained. New features, improvements, and bug fixes are regularly implemented.
- **Future Plans**: The framework will expand to support additional languages like R and JavaScript.
- **Focus of the Framework**: This guide emphasizes the structure and sharing practices of repositories, rather than the specific methodologies or technologies used within the project.
- **Goal**: To ensure your project is understandable, trusted, and easy to use by others, fostering community adoption and collaboration.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## Contact
For any inquiries, feel free to reach out to [Ready_Tensor](...@readytensor.com).

## Acknowledgments








