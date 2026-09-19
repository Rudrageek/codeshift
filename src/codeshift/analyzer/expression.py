from dataclasses import dataclass


@dataclass
class TypeInferenceResult:
    """
    Result of expression type inference.
    """

    type: str | None
    confidence: str
    evidence: str
    parameter_types: dict[str, dict]


def create_result(
    type_name: str | None,
    confidence: str,
    evidence: str,
    parameter_types: dict | None = None,
) -> TypeInferenceResult:
    """
    Create a standardized inference result.
    """

    return TypeInferenceResult(
        type=type_name,
        confidence=confidence,
        evidence=evidence,
        parameter_types=(
            parameter_types
            if parameter_types is not None
            else {}
        ),
    )


def infer_literal(node) -> TypeInferenceResult:
    """
    Infer the type of a JavaScript literal.
    """

    if not node:

        return create_result(
            None,
            "low",
            "No expression provided",
        )

    # ---------------------------------
    # String
    # ---------------------------------

    if node.type == "string":

        return create_result(
            "string",
            "high",
            "expression is a string literal",
        )

    # ---------------------------------
    # Number
    # ---------------------------------

    if node.type in [
        "number",
        "number_literal",
    ]:

        return create_result(
            "number",
            "high",
            "expression is a numeric literal",
        )

    # ---------------------------------
    # Boolean
    # ---------------------------------

    if node.type in [
        "true",
        "false",
    ]:

        return create_result(
            "boolean",
            "high",
            "expression is a boolean literal",
        )

    # ---------------------------------
    # Null
    # ---------------------------------

    if node.type == "null":

        return create_result(
            "null",
            "high",
            "expression is a null literal",
        )

    # ---------------------------------
    # Undefined
    # ---------------------------------

    if node.type == "undefined":

        return create_result(
            "undefined",
            "high",
            "expression is undefined",
        )

    # ---------------------------------
    # Unknown
    # ---------------------------------

    return create_result(
        None,
        "low",
        f"unable to infer type of {node.type} expression",
    )


def infer_binary_expression(
    operation: str,
    left_node,
    right_node,
) -> TypeInferenceResult:
    """
    Infer the type of a JavaScript binary expression.

    Also returns parameter type evidence
    discovered from the expression.
    """

    parameter_types = {}

    # ---------------------------------
    # Comparison operators
    # ---------------------------------

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

                if (
                    left_node
                    and left_node.type == "identifier"
                ):

                    parameter_name = (
                        left_node.text
                        .decode("utf-8")
                    )

                    parameter_types[
                        parameter_name
                    ] = {
                        "type": "number",
                        "confidence": "high",
                        "evidence": (
                            "identifier compared "
                            "with numeric literal"
                        ),
                    }

                return create_result(
                    "boolean",
                    "high",
                    "comparison with numeric literal",
                    parameter_types,
                )

            if right_node.type == "string":

                if (
                    left_node
                    and left_node.type == "identifier"
                ):

                    parameter_name = (
                        left_node.text
                        .decode("utf-8")
                    )

                    parameter_types[
                        parameter_name
                    ] = {
                        "type": "string",
                        "confidence": "high",
                        "evidence": (
                            "identifier compared "
                            "with string literal"
                        ),
                    }

                return create_result(
                    "boolean",
                    "high",
                    "comparison with string literal",
                    parameter_types,
                )

        return create_result(
            "boolean",
            "high",
            f"comparison using operator {operation}",
        )

    # ---------------------------------
    # Arithmetic operators
    # ---------------------------------

    if operation in [
        "-",
        "*",
        "/",
        "%",
    ]:

        # Example:
        #
        # x * 2
        #
        if (
            left_node
            and left_node.type == "identifier"
            and right_node
            and right_node.type in [
                "number",
                "number_literal",
            ]
        ):

            parameter_name = (
                left_node.text
                .decode("utf-8")
            )

            parameter_types[
                parameter_name
            ] = {
                "type": "number",
                "confidence": "high",
                "evidence": (
                    "identifier participates "
                    "in arithmetic with "
                    "numeric literal"
                ),
            }

        # Example:
        #
        # 2 * x
        #
        elif (
            right_node
            and right_node.type == "identifier"
            and left_node
            and left_node.type in [
                "number",
                "number_literal",
            ]
        ):

            parameter_name = (
                right_node.text
                .decode("utf-8")
            )

            parameter_types[
                parameter_name
            ] = {
                "type": "number",
                "confidence": "high",
                "evidence": (
                    "identifier participates "
                    "in arithmetic with "
                    "numeric literal"
                ),
            }

        return create_result(
            "number",
            "high",
            f"arithmetic operation using operator {operation}",
            parameter_types,
        )

    # ---------------------------------
    # Addition
    # ---------------------------------

    if operation == "+":

        # ---------------------------------
        # "Hello " + name
        # ---------------------------------

        if (
            left_node
            and left_node.type == "string"
        ):

            if (
                right_node
                and right_node.type == "identifier"
            ):

                parameter_name = (
                    right_node.text
                    .decode("utf-8")
                )

                parameter_types[
                    parameter_name
                ] = {
                    "type": "string",
                    "confidence": "high",
                    "evidence": (
                        "identifier participates "
                        "in string concatenation"
                    ),
                }

            return create_result(
                "string",
                "high",
                "string literal participates in concatenation",
                parameter_types,
            )

        # ---------------------------------
        # name + "!"
        # ---------------------------------

        if (
            right_node
            and right_node.type == "string"
        ):

            if (
                left_node
                and left_node.type == "identifier"
            ):

                parameter_name = (
                    left_node.text
                    .decode("utf-8")
                )

                parameter_types[
                    parameter_name
                ] = {
                    "type": "string",
                    "confidence": "high",
                    "evidence": (
                        "identifier participates "
                        "in string concatenation"
                    ),
                }

            return create_result(
                "string",
                "high",
                "string literal participates in concatenation",
                parameter_types,
            )

        # ---------------------------------
        # Numeric literal + identifier
        # ---------------------------------

        if (
            left_node
            and left_node.type in [
                "number",
                "number_literal",
            ]
            and right_node
            and right_node.type == "identifier"
        ):

            parameter_name = (
                right_node.text
                .decode("utf-8")
            )

            parameter_types[
                parameter_name
            ] = {
                "type": "number",
                "confidence": "high",
                "evidence": (
                    "identifier participates "
                    "in addition with "
                    "numeric literal"
                ),
            }

            return create_result(
                "number",
                "high",
                "numeric literal participates in addition",
                parameter_types,
            )

        # ---------------------------------
        # Identifier + numeric literal
        # ---------------------------------

        if (
            left_node
            and left_node.type == "identifier"
            and right_node
            and right_node.type in [
                "number",
                "number_literal",
            ]
        ):

            parameter_name = (
                left_node.text
                .decode("utf-8")
            )

            parameter_types[
                parameter_name
            ] = {
                "type": "number",
                "confidence": "high",
                "evidence": (
                    "identifier participates "
                    "in addition with "
                    "numeric literal"
                ),
            }

            return create_result(
                "number",
                "high",
                "numeric literal participates in addition",
                parameter_types,
            )

        # ---------------------------------
        # Numeric literal + numeric literal
        # ---------------------------------

        if (
            left_node
            and right_node
            and left_node.type in [
                "number",
                "number_literal",
            ]
            and right_node.type in [
                "number",
                "number_literal",
            ]
        ):

            return create_result(
                "number",
                "high",
                "two numeric literals participate in addition",
            )

        # ---------------------------------
        # Identifier + identifier
        # ---------------------------------

        if (
            left_node
            and right_node
            and left_node.type == "identifier"
            and right_node.type == "identifier"
        ):

            return create_result(
                "number",
                "medium",
                (
                    "two identifiers participate "
                    "in addition; numeric type "
                    "inferred with medium confidence"
                ),
            )

        return create_result(
            None,
            "low",
            (
                "JavaScript '+' can perform "
                "numeric addition or string "
                "concatenation"
            ),
        )

    # ---------------------------------
    # Unknown operator
    # ---------------------------------

    return create_result(
        None,
        "low",
        (
            f"unable to infer result type "
            f"for operator {operation}"
        ),
    )


def infer_expression(node) -> TypeInferenceResult:
    """
    Infer the type of an arbitrary expression.
    """

    if not node:

        return create_result(
            None,
            "low",
            "No expression provided",
        )

    # ---------------------------------
    # Literal
    # ---------------------------------

    if node.type in [
        "string",
        "number",
        "number_literal",
        "true",
        "false",
        "null",
        "undefined",
    ]:

        return infer_literal(
            node
        )

    # ---------------------------------
    # Binary expression
    # ---------------------------------

    if node.type == "binary_expression":

        operator_node = (
            node.child_by_field_name(
                "operator"
            )
        )

        left_node = (
            node.child_by_field_name(
                "left"
            )
        )

        right_node = (
            node.child_by_field_name(
                "right"
            )
        )

        if not operator_node:

            return create_result(
                None,
                "low",
                "binary expression has no operator",
            )

        operation = (
            operator_node.text
            .decode("utf-8")
        )

        return infer_binary_expression(
            operation,
            left_node,
            right_node,
        )

    # ---------------------------------
    # Unknown expression
    # ---------------------------------

    return create_result(
        None,
        "low",
        (
            f"unsupported expression type: "
            f"{node.type}"
        ),
    )