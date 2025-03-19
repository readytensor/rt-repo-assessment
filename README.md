## GitHub Repository Assessment

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
- **GitPython (>=3.1.44)** – Git repository interactions.  
- **LangChain (>=0.3.20)** – LLM-driven framework.  
- **Pandas (>=2.2.3)** – Data handling.  
- **PyYAML (>=6.0.2)** – Configuration parsing.  

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
   The assessment results can be found in the `Output/repo_name/report.md` file.

**Overall Summary**

- **Total Criteria**: [Total Number of Criteria]
- **Criteria Met**: [Percentage of Criteria Met]

 **Category Breakdown**

| Category      | Criteria Met | Total Criteria | Percentage   |
|---------------|--------------|----------------|--------------|
| Essential     | [Criteria Met for Essential] | [Total Criteria for Essential] | % |
| Professional  | [Criteria Met for Professional] | [Total Criteria for Professional] | % |
| Elite         | [Criteria Met for Elite] | [Total Criteria for Elite] | % |


 **Sample Detailed Results**

| Category            | Criterion                         | Status | Explanation |
|---------------------|-----------------------------------|--------|-------------|
| Code Quality    | Modular Code Organization         | ✅     | This criterion is satisfied in the project by file 'utils.py'. The code is organized into functions and a class, which is a good practice. |. |
| Documentation    | README Completeness               | ✅     | The README provides all necessary information for understanding, setting up, and using the project effectively. |
| Repository Structure | Clear Folder Organization     | ✅     | The repository follows a logical structure with clear divisions for source code, documentation, and other assets. |
| Environment & Dependencies|Test Directory Structure | ❌   | The project directory does not contain a dedicated 'tests/' directory or any other structure that organizes tests in a way that mirrors the main code structure. There is no indication of any testing files or directories present. | |
| License and Legal     | License Presence                  | ✅ | The project directory includes a recognized license file named 'LICENSE.txt' in the root directory, which explicitly states the terms of use, modification, and distribution. |

---
## Data Requirements

### Expected Data Sources and Setup

This project analyzes GitHub repositories by fetching data from the provided repository links. The expected data sources include:
- **GitHub Repository Links**: A list of GitHub repository URLs that the framework will analyze.
  
The repository data consists of:
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

## Configuration

The configuration is managed through the `config.json` and scoring files.

As detailed in the usage section, the config.json defines key parameters like repository URLs and the maximum number of concurrent workers.

### Scoring Criteria 

Scoring is based on five key areas: Documentation, Repository Structure, Environment & Dependencies, License & Legal, and Code Quality. Each criterion is assessed at three levels: **Essential**, **Professional**, and **Elite**.

#### Example: `modular_code_organization.yaml`

```yaml
modular_code_organization:
  name: Modular Code Organization
  description: Code organized into functions/methods.
  essential: true
  professional: true
  elite: true
  include_extensions:
    - .py
    - .ipynb
  aggregation: OR
  based_on: file_content
  prompt: "Ensure code is modular for maintainability."
  ```
#### Logic-based Scoring

Scoring relies on predefined logic through functions that validate, calculate, and measure specific aspects like code length, ensuring consistency in evaluation across repositories.

## Methodology

This project leverages **GPT-4** to provide an advanced, AI-driven framework for GitHub repository assessment. The approach is structured to deliver precise evaluations, blending automated data analysis with intelligent scoring mechanisms.

- **Automated Repository Analysis**: Fetches key data (README, code, metadata) for in-depth quality assessment.
  
- **AI-Enhanced Evaluation**: **GPT-4** augments traditional metrics, delivering context-aware evaluations of code quality, documentation, and structure.

- **Dynamic Scoring Model**: Employs YAML-configured criteria across Documentation, Repository Structure, Environment, License, and Code Quality, ensuring a tiered evaluation system (Essential, Professional, Elite).

- **Precision with Real-Time Validation**: Real-time logic-based scoring, validated by AI prompts, ensures high accuracy in evaluation.

For more on GPT-4, refer to [OpenAI’s GPT-4](https://openai.com/research/gpt-4).

## Performance

Optimized for **speed** and **scalability**:

- **Fast Analysis**: Evaluations typically complete within **few minute**, depending on repo size and network conditions.
- **Parallel Processing**: Supports up to **12 workers** for efficient, simultaneous analysis.
- **Scalable**: Handles large volumes of repositories with minimal latency.
- **GPT-4 Accuracy**: Real-time, high-quality scoring.


## Maintenance Status

- **Current Status**: Actively maintained. New features, improvements, and bug fixes are regularly implemented.
- **Future Plans**: The framework will expand to support additional languages like R and JavaScript.

## Contributing
We welcome contributions to improve the framework. Please refer to the guidelines below for how you can contribute:
1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request with a detailed description of your modifications.

## License

This project is licensed under the [MIT License](https://github.com/readytensor/rt-repo-assessment/blob/main/LICENSE).

For more details, you can view the full [MIT License](https://opensource.org/licenses/MIT).

## Citation

### Research & Best Practices  
- **Ready Tensor, Inc. (2025).** *Best Practices for AI Project Code Repositories.* Retrieved from [Ready Tensor](https://app.readytensor.ai/publications/best-practices-for-ai-project-code-repositories-0llldKKtn8Xb)  
- **LangChain** – [Official Citation](https://docs.langchain.com/docs/citation)  
- **Pandas** – McKinney, W. (2010). *Data Structures for Statistical Computing in Python*. *Proceedings of the 9th Python in Science Conference (SciPy 2010)*, 56–61.  

### Libraries & Tools  
- **GitPython** – Sebastian Thiel et al. (2007). *GitPython: Python Library for Interacting with Git Repositories.* [GitHub](https://github.com/gitpython-developers/GitPython)  
- **LangChain-Community** – Open-source extensions to LangChain. [GitHub](https://github.com/langchain-ai/langchain)  
- **LangChain-OpenAI** – OpenAI integration for LangChain. [Docs](https://python.langchain.com/docs/integrations/llms/openai)  
- **PyYAML** – Kirill Simonov (2006). *PyYAML: YAML Parser and Emitter for Python.* [PyYAML Documentation](https://pyyaml.org/)  
- **python-dotenv** – *Manage environment variables easily.* [GitHub](https://github.com/theskumar/python-dotenv)  
- **Mypy** – *Static type checker for Python.* [GitHub](https://github.com/python/mypy)  


## Contact
For any inquiries, feel free to reach out to [Ready_Tensor](...@readytensor.com).

## Acknowledgments









