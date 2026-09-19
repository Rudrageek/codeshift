from codeshift.transformer.edits import (
    SourceEdit,
    apply_edits,
)


def transform_to_typescript(
    source_code: str,
    analysis_results: list,
) -> str:
    """
    Transform JavaScript into TypeScript using
    source-range edits.

    Type annotations are inserted using source
    positions instead of replacing entire function
    declarations.

    Migration confidence is preserved through
    CodeShift warning comments.
    """

    edits = []

    for result in analysis_results:

        function_name = result["function"]
        parameters = result["parameters"]
        suggestions = result["suggestions"]
        return_type = result["inferred_type"]
        return_confidence = result["confidence"]

        if not function_name:
            continue

        # ---------------------------------
        # Locate function declaration
        # ---------------------------------

        declaration = (
            f"function {function_name}"
            f"({', '.join(parameters)})"
        )

        declaration_start = source_code.find(
            declaration
        )

        if declaration_start == -1:
            continue

        # ---------------------------------
        # Locate parameter section
        # ---------------------------------

        opening_parenthesis = declaration.find("(")

        parameters_start = (
            declaration_start
            + opening_parenthesis
            + 1
        )

        parameters_end = (
            parameters_start
            + len(", ".join(parameters))
        )

        # ---------------------------------
        # Build typed parameters
        # ---------------------------------

        typed_parameters = []
        parameter_warnings = []

        for parameter in parameters:

            parameter_type = "any"
            parameter_confidence = "low"

            for suggestion in suggestions:

                if (
                    suggestion["name"]
                    == parameter
                ):

                    parameter_type = (
                        suggestion["type"]
                    )

                    parameter_confidence = (
                        suggestion["confidence"]
                    )

                    break

            # -----------------------------
            # High confidence
            # -----------------------------

            if parameter_confidence == "high":

                typed_parameters.append(
                    f"{parameter}: {parameter_type}"
                )

            # -----------------------------
            # Medium confidence
            # -----------------------------

            elif parameter_confidence == "medium":

                typed_parameters.append(
                    f"{parameter}: {parameter_type}"
                )

                parameter_warnings.append(
                    f"// CodeShift warning: "
                    f"{parameter} type inferred "
                    f"with medium confidence"
                )

            # -----------------------------
            # Low confidence
            # -----------------------------

            else:

                typed_parameters.append(
                    f"{parameter}: any"
                )

                parameter_warnings.append(
                    f"// CodeShift warning: "
                    f"Could not confidently infer "
                    f"type of {parameter}"
                )

        typed_parameter_string = (
            ", ".join(typed_parameters)
        )

        # ---------------------------------
        # Replace parameter section
        # ---------------------------------

        edits.append(
            SourceEdit(
                start=parameters_start,
                end=parameters_end,
                replacement=typed_parameter_string,
            )
        )

        # ---------------------------------
        # Locate closing parenthesis
        # ---------------------------------

        closing_parenthesis = (
            parameters_start
            + len(", ".join(parameters))
        )

        # ---------------------------------
        # Return type
        # ---------------------------------

        return_type_text = ""

        if return_type:

            return_type_text = (
                f": {return_type}"
            )

            if return_confidence == "medium":

                parameter_warnings.append(
                    "// CodeShift warning: "
                    "return type inferred "
                    "with medium confidence"
                )

            elif return_confidence == "low":

                parameter_warnings.append(
                    "// CodeShift warning: "
                    "return type could not be "
                    "confidently inferred"
                )

        # ---------------------------------
        # Insert return type
        # ---------------------------------

        if return_type_text:

            edits.append(
                SourceEdit(
                    start=closing_parenthesis + 1,
                    end=closing_parenthesis + 1,
                    replacement=return_type_text,
                )
            )

        # ---------------------------------
        # Add warnings
        # ---------------------------------

        if parameter_warnings:

            warning_text = (
                "\n".join(parameter_warnings)
                + "\n"
            )

            edits.append(
                SourceEdit(
                    start=declaration_start,
                    end=declaration_start,
                    replacement=warning_text,
                )
            )

    # ---------------------------------
    # Apply source edits
    # ---------------------------------

    return apply_edits(
        source_code,
        edits,
    )