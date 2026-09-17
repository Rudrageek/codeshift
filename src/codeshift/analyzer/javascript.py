from codeshift.walker.ast import walk_tree

from codeshift.analyzer.type_inference import (
    infer_binary_expression_type,
    infer_literal_type,
    generate_evidence,
)


def analyze_javascript(tree):
    """
    Perform static analysis on a JavaScript AST
    and infer basic TypeScript types with confidence
    and supporting evidence.
    """

    root = tree.root_node
    results = []

    # ---------------------------------
    # Recursively walk through AST
    # ---------------------------------

    for node in walk_tree(root):

        if node.type != "function_declaration":
            continue

        function_name = None
        parameters = []
        return_expression = None
        operation = None
        inferred_type = None
        confidence = "low"
        evidence = "No strong evidence available"

        # ---------------------------------
        # Function name
        # ---------------------------------

        name_node = node.child_by_field_name("name")

        if name_node:
            function_name = name_node.text.decode("utf-8")

        # ---------------------------------
        # Parameters
        # ---------------------------------

        parameters_node = node.child_by_field_name(
            "parameters"
        )

        if parameters_node:

            for parameter in parameters_node.named_children:

                parameters.append(
                    parameter.text.decode("utf-8")
                )

        # ---------------------------------
        # Function body
        # ---------------------------------

        body_node = node.child_by_field_name("body")

        if body_node:

            for statement in body_node.named_children:

                if statement.type != "return_statement":
                    continue

                if not statement.named_children:
                    continue

                expression = statement.named_children[0]

                return_expression = expression.text.decode(
                    "utf-8"
                )

                # ---------------------------------
                # Binary expression
                # ---------------------------------

                if expression.type == "binary_expression":

                    operator_node = (
                        expression.child_by_field_name(
                            "operator"
                        )
                    )

                    if operator_node:

                        operation = operator_node.text.decode(
                            "utf-8"
                        )

                    left_node = (
                        expression.child_by_field_name(
                            "left"
                        )
                    )

                    right_node = (
                        expression.child_by_field_name(
                            "right"
                        )
                    )

                    # Infer expression type
                    (
                        inferred_type,
                        confidence,
                    ) = infer_binary_expression_type(
                        operation,
                        left_node,
                        right_node,
                    )

                    # Generate explanation
                    evidence = generate_evidence(
                        operation,
                        left_node,
                        right_node,
                    )

                # ---------------------------------
                # Literal return
                # ---------------------------------

                else:

                    (
                        inferred_type,
                        confidence,
                    ) = infer_literal_type(
                        expression
                    )

                    evidence = (
                        f"return value is a "
                        f"{inferred_type} literal"
                    )

        # ---------------------------------
        # Infer parameter types
        # ---------------------------------

        parameter_types = {}

        for parameter in parameters:

            parameter_types[parameter] = {
                "type": inferred_type,
                "confidence": confidence,
            }

        # ---------------------------------
        # Comparison inference
        # ---------------------------------

        if (
            operation
            in [
                "==",
                "===",
                "!=",
                "!==",
                ">",
                "<",
                ">=",
                "<=",
            ]
            and body_node
        ):

            for statement in body_node.named_children:

                if statement.type != "return_statement":
                    continue

                if not statement.named_children:
                    continue

                expression = statement.named_children[0]

                if expression.type != "binary_expression":
                    continue

                left_node = (
                    expression.child_by_field_name(
                        "left"
                    )
                )

                right_node = (
                    expression.child_by_field_name(
                        "right"
                    )
                )

                # ---------------------------------
                # Number comparison
                # ---------------------------------

                if right_node and right_node.type in [
                    "number",
                    "number_literal",
                ]:

                    if left_node:

                        left_name = left_node.text.decode(
                            "utf-8"
                        )

                        if left_name in parameter_types:

                            parameter_types[left_name] = {
                                "type": "number",
                                "confidence": "high",
                            }

                # ---------------------------------
                # String comparison
                # ---------------------------------

                if right_node and right_node.type == "string":

                    if left_node:

                        left_name = left_node.text.decode(
                            "utf-8"
                        )

                        if left_name in parameter_types:

                            parameter_types[left_name] = {
                                "type": "string",
                                "confidence": "high",
                            }

        # ---------------------------------
        # String concatenation
        # ---------------------------------

        if operation == "+" and body_node:

            for statement in body_node.named_children:

                if statement.type != "return_statement":
                    continue

                if not statement.named_children:
                    continue

                expression = statement.named_children[0]

                if expression.type != "binary_expression":
                    continue

                left_node = (
                    expression.child_by_field_name(
                        "left"
                    )
                )

                right_node = (
                    expression.child_by_field_name(
                        "right"
                    )
                )

                # ---------------------------------
                # "Hello " + name
                # ---------------------------------

                if (
                    left_node
                    and left_node.type == "string"
                ):

                    if right_node:

                        right_name = (
                            right_node.text.decode(
                                "utf-8"
                            )
                        )

                        if right_name in parameter_types:

                            parameter_types[right_name] = {
                                "type": "string",
                                "confidence": "high",
                            }

                # ---------------------------------
                # name + "!"
                # ---------------------------------

                elif (
                    right_node
                    and right_node.type == "string"
                ):

                    if left_node:

                        left_name = (
                            left_node.text.decode(
                                "utf-8"
                            )
                        )

                        if left_name in parameter_types:

                            parameter_types[left_name] = {
                                "type": "string",
                                "confidence": "high",
                            }

        # ---------------------------------
        # Migration suggestions
        # ---------------------------------

        suggestions = []

        for parameter in parameters:

            parameter_info = parameter_types.get(
                parameter
            )

            if not parameter_info:
                continue

            parameter_type = parameter_info["type"]

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
        # Store analysis result
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