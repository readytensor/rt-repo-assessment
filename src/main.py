import os
from typing import Dict, Any
from config import paths
from utils.llm import get_llm, GPT_4O_MINI
from utils.general import read_yaml_file, write_json_file, read_json_file
from utils.repository import get_readme_content, get_repo_tree, clone_and_extract_repo
from config.scoring.generators import (
    dependancies_criterion_generator,
    license_criterion_generator,
    structure_criterion_generator,
    documentation_criterion_generator,
)
from utils.project_validators import (
    has_readme,
    has_requirements_txt,
    has_pyproject_toml,
    has_setup_py,
    has_license_file,
    has_gitignore_file,
    has_ignored_files,
    get_script_lengths,
)
from code_scorer.code_scorer import score_directory_based_on_files
from config.scoring.generators import get_code_criteria_aggregation_logic

from output_parsers import CriterionScoring
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from report import generate_markdown_report


def get_repo_info(repo_url: str) -> Dict[str, Any]:
    repo_dir_name = os.path.basename(repo_url)
    repo_dir_path = os.path.join(paths.INPUTS_DIR, repo_dir_name)
    clone_and_extract_repo(repo_url=repo_url, output_dir=repo_dir_path)

    readme_exists = has_readme(repo_dir_path)
    requirements_txt_exists = has_requirements_txt(repo_dir_path)
    pyproject_toml_exists = has_pyproject_toml(repo_dir_path)
    setup_py_exists = has_setup_py(repo_dir_path)
    license_file_exists = has_license_file(repo_dir_path)
    gitignore_file_exists = has_gitignore_file(repo_dir_path)
    ignored_files_exist = has_ignored_files(repo_dir_path)
    directory_structure = get_repo_tree(repo_dir_path)
    script_lengths = get_script_lengths(repo_dir_path)

    readme_content = (
        get_readme_content(repo_dir_path) if has_readme(repo_dir_path) else None
    )

    return {
        "readme_exists": readme_exists,
        "requirements_txt_exists": requirements_txt_exists,
        "pyproject_toml_exists": pyproject_toml_exists,
        "setup_py_exists": setup_py_exists,
        "license_file_exists": license_file_exists,
        "gitignore_file_exists": gitignore_file_exists,
        "ignored_files_exist": ignored_files_exist,
        "script_lengths": script_lengths,
        "readme_content": readme_content,
        "directory_structure": directory_structure,
    }


def format_criterion(criterion: dict) -> str:
    return f"""
    # Criterion Name: {criterion['name']}
    # Criterion Description: {criterion['description']}
    """


if __name__ == "__main__":
    prompts = read_yaml_file(paths.PROMPTS_FPATH)
    config = read_json_file(paths.CONFIG_FPATH)

    prompt_template = prompts["scoring_v0"]

    repo_urls = config["urls"]
    max_workers = config["max_workers"]

    for repo_url in repo_urls:
        output_dir = os.path.join(paths.OUTPUTS_DIR, os.path.basename(repo_url))
        os.makedirs(output_dir, exist_ok=True)

        repo_info = get_repo_info(repo_url=repo_url)
        directory_structure = repo_info["directory_structure"]
        readme_content = repo_info["readme_content"]

        del repo_info["directory_structure"]
        del repo_info["readme_content"]

        llm = get_llm(llm=GPT_4O_MINI).with_structured_output(CriterionScoring)

        results = {}

        def process_criterion(
            criterion_id,
            criterion,
            prompt_template,
            repo_info,
            directory_structure,
            readme_content,
            llm,
        ):
            print(f"Scoring criterion: {criterion_id}")
            prompt = prompt_template.format(
                project_info=repo_info,
                directory_structure=directory_structure,
                readme_content=readme_content,
                criterion=format_criterion(criterion),
            )

            response = llm.invoke(prompt).model_dump()
            return criterion_id, response

        aggregation_logic = get_code_criteria_aggregation_logic()
        dir_score, file_scores = score_directory_based_on_files(
            os.path.join(paths.INPUTS_DIR, os.path.basename(repo_url)),
            llm=get_llm(llm=GPT_4O_MINI),
            aggregation_logic=aggregation_logic,
            max_workers=max_workers,
        )

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            process_fn = partial(
                process_criterion,
                prompt_template=prompt_template,
                repo_info=repo_info,
                directory_structure=directory_structure,
                readme_content=readme_content,
                llm=llm,
            )

            for generator in [
                documentation_criterion_generator,
                structure_criterion_generator,
                dependancies_criterion_generator,
                license_criterion_generator,
            ]:
                for criterion_id, response in executor.map(
                    lambda x: process_fn(x[0], x[1]), generator()
                ):
                    results[criterion_id] = response
                    write_json_file(
                        os.path.join(output_dir, "assessment.json"), results
                    )

        results = {**results, **dir_score}

        write_json_file(os.path.join(output_dir, "assessment.json"), results)
        write_json_file(os.path.join(output_dir, "file_scores.json"), file_scores)

        # generate_markdown_report(
        #     assessment=results,
        #     file_scores=file_scores,
        #     output_file=os.path.join(output_dir, "report.md"),
        # )
