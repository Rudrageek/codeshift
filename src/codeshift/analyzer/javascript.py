from codeshift.walker.ast import walk_tree

from codeshift.analyzer.expression import (
    infer_expression,
)


def analyze_javascript(tree):
    """
    Perform static analysis on a JavaScript AST.

    The analyzer identifies function declarations,
    parameters, return expressions, inferred types,
    confidence levels, evidence, and migration
    suggestions.
    """

    root = tree.root_node

    results = []

    # ---------------------------------
    # Walk through AST
    # ---------------------------------

    for node in walk_tree(root):

        if node.type != "function_declaration":
            continue

        function_name = None
        parameters = []
        return_expression = None

        inferred_type = None
        confidence = "low"
        evidence = "No strong evidence available"

        operation = None
        operator_node = None

        # ---------------------------------
        # Function name
        # ---------------------------------

        name_node = node.child_by_field_name(
            "name"
        )

        if name_node:

            function_name = (
                name_node.text
                .decode("utf-8")
            )

        # ---------------------------------
        # Parameters
        # ---------------------------------

        parameters_node = (
            node.child_by_field_name(
                "parameters"
            )
        )

        if parameters_node:

            for parameter in (
                parameters_node.named_children
            ):

                parameters.append(
                    parameter.text
                    .decode("utf-8")
                )

        # ---------------------------------
        # Function body
        # ---------------------------------

        body_node = node.child_by_field_name(
            "body"
        )

        return_node = None

        if body_node:

            for statement in (
                body_node.named_children
            ):

                if (
                    statement.type
                    != "return_statement"
                ):
                    continue

                if not statement.named_children:
                    continue

                return_node = (
                    statement.named_children[0]
                )

                return_expression = (
                    return_node.text
                    .decode("utf-8")
                )

                break

        # ---------------------------------
        # Expression inference
        # ---------------------------------

        inferred_parameter_types = {}

        if return_node:

            inference = infer_expression(
                return_node
            )

            inferred_type = (
                inference.type
            )

            confidence = (
                inference.confidence
            )

            evidence = (
                inference.evidence
            )

            inferred_parameter_types = (
                inference.parameter_types
            )

        # ---------------------------------
        # Parameter type inference
        # ---------------------------------

        parameter_types = {}

        for parameter in parameters:

            parameter_types[parameter] = {
                "type": inferred_type,
                "confidence": confidence,
            }

            # ---------------------------------
            # Override with expression evidence
            # ---------------------------------

            if parameter in (
                inferred_parameter_types
            ):

                parameter_types[parameter] = (
                    inferred_parameter_types[
                        parameter
                    ]
                )

        # ---------------------------------
        # Extract operation
        # ---------------------------------

        if (
            return_node
            and return_node.type
            == "binary_expression"
        ):

            operator_node = (
                return_node.child_by_field_name(
                    "operator"
                )
            )

            if operator_node:

                operation = (
                    operator_node.text
                    .decode("utf-8")
                )

        # ---------------------------------
        # Migration suggestions
        # ---------------------------------

        suggestions = []

        for parameter in parameters:

            parameter_info = (
                parameter_types.get(
                    parameter
                )
            )

            if not parameter_info:
                continue

            parameter_type = (
                parameter_info["type"]
            )

            parameter_confidence = (
                parameter_info["confidence"]
            )

            if parameter_type:

                suggestions.append(
                    {
                        "name": parameter,
                        "type": parameter_type,
                        "confidence": parameter_confidence,
                    }
                )

        # ---------------------------------
        # Store result
        # ---------------------------------

        results.append(
            {
                "function": function_name,
                "parameters": parameters,
                "return_expression": return_expression,
                "operation": operation,
                "inferred_type": inferred_type,
                "confidence": confidence,
                "evidence": evidence,
                "suggestions": suggestions,
            }
        )

    return results