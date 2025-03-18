import os
import tiktoken
import concurrent.futures
from config import paths
from dotenv import load_dotenv
from typing import List, Dict, Any, Tuple, Union
from utils.general import read_yaml_file
from langchain_core.documents import Document
from generators import get_instructions
from output_parsers import get_content_based_scoring_model
from directory_scorer.tree import build_tree, post_order_generator
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_community.document_loaders import (
    NotebookLoader,
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)

load_dotenv()

dir_path = os.path.dirname((os.path.abspath(__file__)))
extensions = read_yaml_file(paths.TRACKED_FILES_FPATH)
scoring_file_prompt = read_yaml_file(paths.PROMPTS_FPATH)["score_file"]

tracked_extensions = extensions["tracked_extensions"]
text_extensions = extensions["text_extensions"]
ignored_names = extensions["ignored_names"]

instructions = get_instructions(content_based_only=True)


def count_tokens(text: str, model_name: str = "gpt-4") -> int:
    """
    Count the number of tokens in a text string for a specific model.

    Args:
        text (str): The text to count tokens for.
        model_name (str): The name of the model to use for token counting.
            Defaults to "gpt-4".

    Returns:
        int: The number of tokens in the text.
    """
    encoding = tiktoken.encoding_for_model(model_name)
    tokens = encoding.encode(text)
    return len(tokens)


def score_file(
    file_path: str,
    llm: BaseChatModel,
    chunk_size: int = 128000,
    chunk_overlap: int = 200,
    max_token_count: int = 128_000,
    global_context: str = "",
) -> Dict[str, Any]:
    """
    Score a file's code quality using a language model.

    Args:
        file_path (str): The path to the file to score.
        llm (BaseChatModel): The language model to use for scoring.
        chunk_size (int): The size of each text chunk when splitting the file content.
        chunk_overlap (int): The overlap between text chunks to maintain context.
        max_token_count (int): Maximum allowed tokens. Files exceeding this will be skipped.
        global_context (str): Additional context about the codebase to help inform scoring.

    Returns:
        str: The summarized content."""
    documents = load_document(file_path)

    # add global context as the first document in the list
    if global_context:
        documents.insert(0, Document(page_content=global_context))

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    splits = text_splitter.split_documents(documents)

    # check if the document is too long using max_str_length
    combined_text = "".join([split.page_content for split in splits])
    tokens = count_tokens(combined_text, model_name="gpt-4o")
    if tokens > max_token_count:
        print(f"Skipping document as it is too long {file_path} ({tokens} tokens)")
        return {}

    if tokens == 0:
        print(f"Skipping document as it is empty {file_path}")
        return {}

    prompts = [
        scoring_file_prompt.format(
            file_content=split.page_content, instructions=instructions
        )
        for split in splits
    ]

    file_extension = os.path.splitext(file_path)[-1].lower()

    CodeQualityFileScoring = get_content_based_scoring_model(file_extension)

    results = (
        llm.with_structured_output(CodeQualityFileScoring).invoke(prompts).model_dump()
    )
    results["file_path"] = file_path
    return results


def load_document(file_path) -> List[Document]:
    """
    Load the document based on file type.

    Args:
        file_path (str): The path to the file to load.

    Returns:
        List[Document]: A list of Document objects containing the file content.

    Raises:
        ValueError: If the file type is not supported.
    """
    ext = os.path.splitext(file_path)[-1].lower()

    # Initialize loader variable with correct type
    loader: Union[PyPDFLoader, Docx2txtLoader, NotebookLoader, TextLoader]

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".docx":
        loader = Docx2txtLoader(file_path)
    elif ext == ".ipynb":
        loader = NotebookLoader(file_path)
    elif ext in text_extensions:
        loader = TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    documents = loader.load()
    return documents


def score_directory_based_on_files(
    directory_path: str,
    llm: BaseChatModel,
    aggregation_logic: Dict[str, str],
    chunk_size: int = 128000,
    chunk_overlap: int = 200,
    max_token_count: int = 128000,
    tracked_extensions: List[str] = tracked_extensions,
    ignored_names: List[str] = ignored_names,
    global_context: str = "",
    max_workers: int = 4,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Score all files in a directory based on code quality criteria.

    Args:
        directory_path (str): The path to the directory to analyze.
        llm (BaseChatModel): The language model to use for scoring.
        aggregation_logic (Dict[str, str]): The aggregation logic to use for scoring.
        chunk_size (int): The size of each text chunk when splitting file content.
        chunk_overlap (int): The overlap between text chunks to maintain context.
        max_token_count (int): Maximum allowed tokens per file. Files exceeding this will be skipped.
        tracked_extensions (List[str]): File extensions to analyze.
        ignored_names (List[str]): File/directory names to ignore.
        global_context (str): Additional context about the codebase to help inform scoring.
        max_workers (int): Maximum number of parallel workers to use.

    Returns:
        Tuple[Dict[str, Any], List[Dict[str, Any]]]: A tuple containing:
            - Combined scores across all files
            - List of individual file scores
    """

    root = build_tree(
        directory_path,
        ignored_names=ignored_names,
        tracked_extensions=tracked_extensions,
        global_context=global_context,
    )

    if root.is_dir and not root.children:
        print(f"Skipping directory as it is empty {directory_path}")
        raise ValueError("Cannot summarize an empty directory.")

    # Collect all non-directory nodes to process
    files_to_score = []
    for node in post_order_generator(root):
        if not node.is_dir:
            files_to_score.append(node)

    all_scores = []

    # Define a worker function to score a single file
    def score_file_worker(node):
        print(f"Scoring {node.name}")
        return score_file(
            node.full_path,
            llm=llm,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            max_token_count=max_token_count,
            global_context=node.global_context,
        )

    # Process files in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {
            executor.submit(score_file_worker, node): node for node in files_to_score
        }
        for future in concurrent.futures.as_completed(future_to_file):
            try:
                score = future.result()
                if score != {}:
                    all_scores.append(score)
            except Exception as exc:
                node = future_to_file[future]
                print(f"Error scoring {node.name}: {exc}")

    directory_scores = combine_scores(all_scores, aggregation_logic)
    return directory_scores, all_scores


def combine_scores(
    file_scores: List[Dict[str, Any]], aggregation_logic: Dict[str, str]
) -> Dict[str, Any]:
    """
    Combine individual file scores into an overall score based on aggregation logic.

    Args:
        file_scores (List[Dict[str, Any]]): List of individual file scores.
        aggregation_logic (Dict[str, str]): Dictionary mapping criteria to aggregation logic.
            Supported values are "OR" and "AND".

    Returns:
        Dict[str, Any]: Combined scores across all files.

    Notes:
        - "OR" logic: If any file satisfies the criterion, the combined score is 1.
        - "AND" logic: All files must satisfy the criterion for the combined score to be 1.
    """
    # Collect all unique criteria from all files
    all_criteria = set()
    for file_score in file_scores:
        all_criteria.update(file_score["scores"].keys())

    # Initialize combined scores with all criteria set to 0
    combined_scores = {
        criterion: {
            "score": 0,
            "explanation": "Not satisfied by any files in the project.",
        }
        for criterion in all_criteria
    }

    # Iterate over each criterion
    for criterion in combined_scores.keys():
        logic = aggregation_logic.get(criterion, "OR")

        if logic == "OR":
            # OR logic: If any file satisfies the criterion, update the combined score
            satisfied_files = []
            for file_score in file_scores:
                # Skip if this file doesn't have this criterion
                if criterion not in file_score["scores"]:
                    continue

                if file_score["scores"][criterion]["score"] == 1:
                    file_name = os.path.basename(file_score["file_path"])
                    satisfied_files.append(
                        file_score["scores"][criterion]["explanation"]
                    )
                    combined_scores[criterion] = {
                        "score": 1,
                        "explanation": f"This criterion is satisfied in the project by file '{file_name}'. {file_score['scores'][criterion]['explanation']}",
                    }
                    break  # No need to check further if one file satisfies
        elif logic == "AND":
            # Initialize the score to 1, assuming all files satisfy the criterion
            combined_scores[criterion]["score"] = 1
            combined_scores[criterion][
                "explanation"
            ] = "This criterion is consistently satisfied throughout the project."

            # Collect explanations for files that do not satisfy the criterion
            failure_explanations = []

            # Check each file's score
            for file_score in file_scores:
                # Skip if this file doesn't have this criterion
                if criterion not in file_score["scores"]:
                    continue

                if file_score["scores"][criterion]["score"] == 0:
                    file_name = os.path.basename(file_score["file_path"])
                    failure_explanations.append(
                        f"{file_name}: {file_score['scores'][criterion]['explanation']}"
                    )
                    combined_scores[criterion]["score"] = 0

            # If there are any failures, update the explanation
            if failure_explanations:
                combined_scores[criterion]["explanation"] = (
                    "This criterion is not consistently satisfied. Issues include: "
                    + "; ".join(
                        failure_explanations[
                            :3
                        ]  # Limit to first 3 explanations to avoid overly long text
                    )
                )
                if len(failure_explanations) > 3:
                    combined_scores[criterion][
                        "explanation"
                    ] += f" and {len(failure_explanations) - 3} more issues."

    return combined_scores
