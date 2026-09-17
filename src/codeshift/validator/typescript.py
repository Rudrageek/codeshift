from tree_sitter import Language, Parser
import tree_sitter_typescript


def validate_typescript(source_code: str) -> dict:
    """
    Validate generated TypeScript syntax using
    Tree-sitter's TypeScript grammar.

    Returns:
        {
            "valid": bool,
            "errors": list[str]
        }
    """

    # ---------------------------------
    # Load TypeScript language
    # ---------------------------------

    typescript_language = Language(
        tree_sitter_typescript.language_typescript()
    )

    parser = Parser(
        typescript_language
    )

    # ---------------------------------
    # Parse TypeScript
    # ---------------------------------

    tree = parser.parse(
        source_code.encode("utf-8")
    )

    root = tree.root_node

    errors = []

    # ---------------------------------
    # Recursively find ERROR nodes
    # ---------------------------------

    def find_errors(node):

        if node.type == "ERROR":

            text = node.text.decode(
                "utf-8"
            )

            errors.append(
                f"Syntax error near: {text[:80]}"
            )

        for child in node.children:
            find_errors(child)

    find_errors(root)

    # ---------------------------------
    # Validation result
    # ---------------------------------

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }