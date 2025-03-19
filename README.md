# Github Repository Assessment 

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

## Installation

### Using `uv` for Package & Project Management  
This project uses `uv`[uv](https://docs.astral.sh/uv) for fast and efficient Python package management.

1. **Install `uv`**  
   Run the following command to install `uv`:
   ```bash
   pip install uv
   ```

   [How to install uv](https://docs.astral.sh/uv/getting-started/installation/)

2. **Install Python & Dependencies**
   Set up Python and install all dependencies in a virtual environment using:  
   ```bash
   make install
   ```

3. **Adding New Packages**  
   To add a package to the project, use the following command:
   ```bash
   uv add <package>
   ```

## Usage  

1.**Run the Assessment** 
  Execute the repository assessment tool using:  
  ```bash
  python main.py --config config.json
  ```
2.**Configure Repository URLs & Max Workers**
  Modify config.json to specify repository URLs:
  ```bash
  {
  "urls": [
    "https://github.com/XingangPan/DragGAN"
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

| Category      | Criteria Met | Total Criteria | Percentage |
|---------------|--------------|----------------|------------|
| Essential     | [Criteria Met for Essential] | [Total Criteria for Essential] | [Percentage] |
| Professional  | [Criteria Met for Professional] | [Total Criteria for Professional] | [Percentage] |
| Elite         | [Criteria Met for Elite] | [Total Criteria for Elite] | [Percentage] |

---

### Code Quality: [Rating]
- [Description of Code Quality Assessment]

### Documentation: [Rating]
- [Description of Documentation Assessment]

### Repository Structure: [Rating]
- [Description of Repository Structure Assessment]

### Environment & Dependencies: [Rating]
- [Description of Environment & Dependencies Assessment]

### License & Legal: [Rating]
- [Description of License & Legal Assessment]




## Install

### uv

This project uses [uv](https://docs.astral.sh/uv) for python package and project management.

[How to install uv](https://docs.astral.sh/uv/getting-started/installation/)

### python and dependencies

Install python and dependencies in a virtual environment.

```bash
make install
```

To add a package to the project, use `uv add` command to install the package in the virtual environment.

```bash
uv add <package>
```