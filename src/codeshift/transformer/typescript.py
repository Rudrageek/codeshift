def transform_to_typescript(
    source_code: str,
    analysis_results: list
) -> str:
    """
    Convert analyzed JavaScript functions into TypeScript.

    Transformation policy:
        HIGH   -> automatic migration
        MEDIUM -> migration with warning comment
        LOW    -> keep original parameter type as any
    """

    transformed_code = source_code

    for result in analysis_results:
        function_name = result["function"]
        parameters = result["parameters"]
        suggestions = result["suggestions"]
        return_type = result["inferred_type"]
        return_confidence = result["confidence"]

        if not function_name:
            continue

        typed_parameters = []
        warnings = []

        # ---------------------------------
        # Process parameters
        # ---------------------------------

        for parameter in parameters:

            parameter_type = "any"
            parameter_confidence = "low"

            for suggestion in suggestions:
                if suggestion["name"] == parameter:
                    parameter_type = suggestion["type"]
                    parameter_confidence = suggestion["confidence"]
                    break

            # High confidence
            if parameter_confidence == "high":
                typed_parameters.append(
                    f"{parameter}: {parameter_type}"
                )

            # Medium confidence
            elif parameter_confidence == "medium":
                typed_parameters.append(
                    f"{parameter}: {parameter_type}"
                )

                warnings.append(
                    f"// CodeShift warning: "
                    f"{parameter} type inferred with medium confidence"
                )

            # Low confidence
            else:
                typed_parameters.append(
                    f"{parameter}: any"
                )

                warnings.append(
                    f"// CodeShift warning: "
                    f"Could not confidently infer type of {parameter}"
                )

        typed_parameters_string = ", ".join(
            typed_parameters
        )

        # ---------------------------------
        # Original declaration
        # ---------------------------------

        original_declaration = (
            f"function {function_name}"
            f"({', '.join(parameters)})"
        )

        # ---------------------------------
        # Return type handling
        # ---------------------------------

        if return_type:

            typescript_declaration = (
                f"function {function_name}"
                f"({typed_parameters_string})"
                f": {return_type}"
            )

            if return_confidence == "medium":
                warnings.append(
                    f"// CodeShift warning: "
                    f"return type inferred with medium confidence"
                )

            elif return_confidence == "low":
                warnings.append(
                    f"// CodeShift warning: "
                    f"return type could not be confidently inferred"
                )

        else:

            typescript_declaration = (
                f"function {function_name}"
                f"({typed_parameters_string})"
            )

        # ---------------------------------
        # Add warnings above function
        # ---------------------------------

        replacement = typescript_declaration

        if warnings:
            replacement = (
                "\n".join(warnings)
                + "\n"
                + typescript_declaration
            )

        # ---------------------------------
        # Apply transformation
        # ---------------------------------

        transformed_code = transformed_code.replace(
            original_declaration,
            replacement,
            1,
        )

    return transformed_code