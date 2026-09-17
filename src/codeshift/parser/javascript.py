from tree_sitter import Language, Parser
import tree_sitter_javascript


def parse_javascript(source_code: str):
    """
    Parse JavaScript source code and return the AST.
    """

    javascript_language = Language(
        tree_sitter_javascript.language()
    )

    parser = Parser(javascript_language)

    tree = parser.parse(
        source_code.encode("utf-8")
    )

    return tree


def print_ast(tree):
    """
    Print the AST as a tree structure.
    """

    print(tree.root_node)