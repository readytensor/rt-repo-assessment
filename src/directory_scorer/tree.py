import os
from pathlib import Path
from typing import Generator, List, Optional
from logger import get_logger

logger = get_logger(__name__)


class TreeNode:
    """
    A node in a file system tree structure.

    Represents either a file or directory in the file system, maintaining parent-child relationships
    and providing methods for tree manipulation and summary storage.

    Attributes:
        name (str): The name of the file or directory.
        full_path (str): The absolute path to the file or directory.
        is_dir (bool): Whether this node represents a directory.
        children (List["TreeNode"]): Child nodes of this node.
        summary (str): A summary of the file or directory content.
        parent (Optional["TreeNode"]): The parent node of this node.
        global_context (str): Additional context about the codebase.
    """

    def __init__(
        self,
        name: str,
        full_path: str,
        is_dir: bool,
        parent: Optional["TreeNode"] = None,
        global_context: str = "",
    ):
        """
        Initialize a TreeNode.

        Args:
            name (str): The name of the file or directory.
            full_path (str): The absolute path to the file or directory.
            is_dir (bool): Whether this node represents a directory.
            parent (Optional["TreeNode"], optional): The parent node. Defaults to None.
            global_context (str, optional): Additional context about the codebase. Defaults to "".
        """
        self.name = name
        self.full_path = full_path
        self.is_dir = is_dir
        self.children: List["TreeNode"] = []
        self.summary: str = ""
        self.parent = parent
        self.global_context = global_context

    def add_child(self, child: "TreeNode"):
        """
        Add a child node to this node.

        Args:
            child (TreeNode): The child node to add.
        """
        child.parent = self
        self.children.append(child)

    def __str__(self):
        """
        Return a string representation of this node.

        Returns:
            str: A string representation of this node.
        """
        return f"TreeNode: {self.name}"

    def save_summary(self, output_dir: Optional[str] = None):
        """
        Save the summary of this node to a file.

        Args:
            output_dir (Optional[str], optional): The directory to save the summary to. Defaults to None.

        Raises:
            ValueError: If output_dir is None.
        """
        if output_dir is None:
            raise ValueError("output_dir is required for saving summary")

        file_path = Path(self.full_path).name
        temp_node = self
        while temp_node.parent is not None:
            file_path = os.path.join(temp_node.parent.name, file_path)
            temp_node = temp_node.parent

        file_path = os.path.join(output_dir, f"{file_path}.txt")
        if self.is_dir:
            name = Path(file_path).name.split(".")[0]
            file_path = os.path.join(
                os.path.dirname(file_path), name, f"directory_summary.txt"
            )
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name, exist_ok=True)

        with open(file_path, "w") as f:
            f.write(self.summary)


def post_order_generator(node: TreeNode) -> Generator[TreeNode, None, None]:
    """
    Generate nodes in post-order traversal (children first, then parent).

    Args:
        node (TreeNode): The root node to start traversal from.

    Yields:
        TreeNode: Each node in the tree in post-order.
    """
    for child in node.children:
        yield from post_order_generator(child)

    yield node


def build_tree(
    path: str,
    tracked_extensions: List[str],
    parent: Optional[TreeNode] = None,
    ignored_names: List[str] = [],
    global_context: str = "",
) -> Optional[TreeNode]:
    """
    Build a tree structure from a file system path.

    Args:
        path (str): The path to build the tree from.
        tracked_extensions (List[str]): List of file extensions to include in the tree.
        parent (Optional[TreeNode], optional): The parent node. Defaults to None.
        ignored_names (List[str], optional): List of file/directory names to ignore. Defaults to [].
        global_context (str, optional): Additional context about the codebase. Defaults to "".

    Returns:
        Optional[TreeNode]: The root node of the built tree, or None if the path should be ignored.
    """
    name = os.path.basename(path)
    is_dir = os.path.isdir(path)
    node = TreeNode(name, path, is_dir, parent, global_context)

    if name in ignored_names:
        return None

    if not is_dir and not any([name.endswith(i) for i in tracked_extensions]):
        return None

    if is_dir:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            child_node = build_tree(
                item_path,
                parent=node,
                tracked_extensions=tracked_extensions,
                ignored_names=ignored_names,
                global_context=global_context,
            )
            if child_node is not None:
                node.add_child(child_node)

    return node


def print_tree(node: TreeNode) -> None:
    """
    Print a visual representation of the tree structure.

    Args:
        node (TreeNode): The root node to print from.
    """
    prefix = "📁 " if node.is_dir else "📄 "
    logger.info("  " + f"{prefix}{node.name} ({node.full_path})")

    for child in node.children:
        print_tree(child)
