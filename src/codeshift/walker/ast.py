from tree_sitter import Node


def walk_tree(node: Node):
    """
    Recursively walk through every node in a Tree-sitter AST.

    Yields each AST node one by one.
    """

    yield node

    for child in node.children:
        yield from walk_tree(child)