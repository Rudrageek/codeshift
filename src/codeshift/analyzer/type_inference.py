def infer_binary_expression_type(
    operation: str,
    left_node,
    right_node,
) -> tuple[str | None, str]:
    """
    Infer the result type of a JavaScript binary expression.

    Returns:
        (type, confidence)
    """

    if operation in [
        "==",
        "===",
        "!=",
        "!==",
        ">",
        "<",
        ">=",
        "<=",
    ]:
        return "boolean", "high"

    if operation in [
        "-",
        "*",
        "/",
        "%",
    ]:
        return "number", "high"

    if operation == "+":
        if (
            left_node
            and left_node.type == "string"
        ) or (
            right_node
            and right_node.type == "string"
        ):
            return "string", "high"

        if (
            left_node
            and right_node
            and left_node.type == "identifier"
            and right_node.type == "identifier"
        ):
            return "number", "medium"

        return "number", "medium"

    return None, "low"


def infer_literal_type(node) -> tuple[str | None, str]:
    """
    Infer the TypeScript type of a JavaScript literal.

    Returns:
        (type, confidence)
    """

    if not node:
        return None, "low"

    if node.type == "string":
        return "string", "high"

    if node.type in [
        "number",
        "number_literal",
    ]:
        return "number", "high"

    if node.type in [
        "true",
        "false",
    ]:
        return "boolean", "high"

    return None, "low"


def generate_evidence(
    operation: str,
    left_node,
    right_node,
) -> str:
    """
    Generate a human-readable explanation
    for why a type was inferred.
    """

    if operation in [
        "==",
        "===",
        "!=",
        "!==",
        ">",
        "<",
        ">=",
        "<=",
    ]:
        if right_node:
            if right_node.type in [
                "number",
                "number_literal",
            ]:
                value = right_node.text.decode("utf-8")

                return (
                    f"comparison with numeric literal {value}"
                )

            if right_node.type == "string":
                value = right_node.text.decode("utf-8")

                return (
                    f"comparison with string literal {value}"
                )

        return (
            f"comparison using operator {operation}"
        )

    if operation in [
        "-",
        "*",
        "/",
        "%",
    ]:
        return (
            f"arithmetic operation using operator {operation}"
        )

    if operation == "+":
        if (
            left_node
            and left_node.type == "string"
        ):
            return (
                "string literal participates in concatenation"
            )

        if (
            right_node
            and right_node.type == "string"
        ):
            return (
                "string literal participates in concatenation"
            )

        if (
            left_node
            and right_node
            and left_node.type == "identifier"
            and right_node.type == "identifier"
        ):
            return (
                "two identifiers participate in addition; "
                "numeric type inferred with medium confidence"
            )

        return (
            "addition operator; JavaScript '+' can perform "
            "numeric addition or string concatenation"
        )

    return (
        f"unable to establish strong evidence for "
        f"operator {operation}"
    )