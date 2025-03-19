import os
from typing import Dict, Any
from logger import get_logger
from config import paths
from utils.llm import get_llm, GPT_4O_MINI
from utils.general import read_yaml_file, write_json_file, read_json_file
from utils.repository import (
    get_readme_content,
    get_repo_tree,
    download_and_extract_repo,
    clone_repo,
    is_repo_public,
)
from generators import (
    get_aggregation_logic,
    get_criteria_by_type,
    get_criteria_names,
    get_category_criteria,
    get_instructions,
    logic_based_criterion_generator,
    metadata_based_criterion_generator,
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
from config.logic_based_scoring import logic_based_scoring
from directory_scorer.content_based_scorer import score_directory_based_on_files
from output_parsers import CriterionScoring
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from report import generate_markdown_report
from generators import get_criteria_args

criteria_args = get_criteria_args()
logger = get_logger(__name__)


def get_repo_metadata(repo_url: str) -> Dict[str, Any]:
    repo_dir_name = os.path.basename(repo_url)
    repo_dir_path = os.path.join(paths.INPUTS_DIR, repo_dir_name)
    retry_attempts = 0
    while retry_attempts < 3:
        try:
            if is_repo_public(repo_url):
                download_and_extract_repo(repo_url=repo_url, output_dir=repo_dir_path)
            else:
                clone_repo(repo_url=repo_url, output_dir=repo_dir_path)
            break
        except Exception as e:
            logger.error(f"Error cloning and extracting repo {repo_url}: {e}")
            retry_attempts += 1

    readme_exists = has_readme(repo_dir_path)
    requirements_txt_exists = has_requirements_txt(repo_dir_path)
    pyproject_toml_exists = has_pyproject_toml(repo_dir_path)
    setup_py_exists = has_setup_py(repo_dir_path)
    license_file_exists = has_license_file(repo_dir_path)
    gitignore_file_exists = has_gitignore_file(repo_dir_path)
    ignored_files_exist = has_ignored_files(repo_dir_path)
    directory_structure = get_repo_tree(repo_dir_path)
    script_lengths = get_script_lengths(repo_dir_path)

    readme_content = get_readme_content(repo_dir_path) if readme_exists else None

    return {
        "repository_name": os.path.basename(repo_url),
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
    criteria_types = get_criteria_by_type()

    prompt_template = prompts["scoring_v0"]

    repo_urls = config["urls"]
    max_workers = config["max_workers"]

    for repo_url in repo_urls:
        output_dir = os.path.join(paths.OUTPUTS_DIR, os.path.basename(repo_url))
        os.makedirs(output_dir, exist_ok=True)

        metadata = get_repo_metadata(repo_url=repo_url)
        directory_structure = metadata["directory_structure"]
        readme_content = metadata["readme_content"]

        del metadata["directory_structure"]
        del metadata["readme_content"]

        llm = get_llm(llm=GPT_4O_MINI).with_structured_output(CriterionScoring)

        results = {}

        for criterion_id, criterion in logic_based_criterion_generator():
            results[criterion_id] = logic_based_scoring[criterion_id](
                metadata, **criteria_args[criterion_id]
            )

        def process_criterion(
            criterion_id,
            criterion,
            prompt_template,
            metadata,
            directory_structure,
            readme_content,
            llm,
        ):
            logger.info(f"Scoring criterion: {criterion_id}")
            prompt = prompt_template.format(
                project_info=metadata,
                directory_structure=directory_structure,
                readme_content=readme_content,
                criterion=format_criterion(criterion),
                instructions=get_instructions(criterion_id=criterion_id),
            )
            response = llm.invoke(prompt).model_dump()
            return criterion_id, response

        aggregation_logic = get_aggregation_logic()
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
                metadata=metadata,
                directory_structure=directory_structure,
                readme_content=readme_content,
                llm=llm,
            )

            for criterion_id, response in executor.map(
                lambda x: process_fn(x[0], x[1]), metadata_based_criterion_generator()
            ):
                results[criterion_id] = response
                write_json_file(os.path.join(output_dir, "assessment.json"), results)

        results = {**results, **dir_score}

        write_json_file(os.path.join(output_dir, "assessment.json"), results)
        write_json_file(os.path.join(output_dir, "file_scores.json"), file_scores)

        generate_markdown_report(
            assessment=results,
            output_file=os.path.join(output_dir, "report.md"),
            criteria_types=criteria_types,
            criteria_names=get_criteria_names(),
            category_criteria=get_category_criteria(),
        )
