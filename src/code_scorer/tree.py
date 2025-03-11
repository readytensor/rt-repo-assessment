import os
from pathlib import Path
from typing import Generator, List


class TreeNode:
    def __init__(
        self,
        name: str,
        full_path: str,
        is_dir: bool,
        parent: "TreeNode" = None,
        global_context: str = "",
    ):
        self.name = name
        self.full_path = full_path
        self.is_dir = is_dir
        self.children: List["TreeNode"] = []
        self.summary: str = None
        self.parent = parent
        self.global_context = global_context

    def add_child(self, child: "TreeNode"):
        child.parent = self
        self.children.append(child)

    def __str__(self):
        return f"TreeNode: {self.name}"

    def save_summary(self, output_dir: str = None):
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
    for child in node.children:
        yield from post_order_generator(child)

    yield node


def build_tree(
    path: str,
    tracked_extensions: List[str],
    parent: TreeNode = None,
    ignored_names: List[str] = [],
    global_context: str = "",
) -> TreeNode:
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
    prefix = "📁 " if node.is_dir else "📄 "
    print("  " + f"{prefix}{node.name} ({node.full_path})")

    for child in node.children:
        print_tree(child)
