import typer

from codeshift.parser.javascript import (
    parse_javascript,
    print_ast,
)

from codeshift.analyzer.javascript import (
    analyze_javascript,
)

from codeshift.transformer.typescript import (
    transform_to_typescript,
)

from codeshift.validator.typescript import (
    validate_typescript,
)


app = typer.Typer(
    name="codeshift",
    help="AI-assisted code migration and static analysis tool.",
)


@app.callback()
def main():
    """CodeShift CLI."""
    pass


@app.command()
def analyze(
    file: str = typer.Argument(
        ...,
        help="Path to the source code file"
    ),
    output: str = typer.Option(
        None,
        "--output",
        "-o",
        help="Output TypeScript file"
    )
):
    """Analyze a JavaScript source code file."""

    # -------------------------
    # Read source file
    # -------------------------

    try:

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            source_code = f.read()

    except FileNotFoundError:

        typer.echo(
            f"Error: File not found: {file}"
        )

        raise typer.Exit(
            code=1
        )

    # -------------------------
    # Parse JavaScript
    # -------------------------

    tree = parse_javascript(
        source_code
    )

    typer.echo(
        "✓ JavaScript parsed successfully"
    )

    typer.echo(
        f"Root node: {tree.root_node.type}"
    )

    # -------------------------
    # Print AST
    # -------------------------

    typer.echo(
        "\nAST:"
    )

    print_ast(
        tree
    )

    # -------------------------
    # Static analysis
    # -------------------------

    results = analyze_javascript(
        tree
    )

    typer.echo(
        "\nStatic Analysis:"
    )

    typer.echo(
        "────────────────────────"
    )

    if not results:

        typer.echo(
            "No function declarations found."
        )

        return

    for result in results:

        # -------------------------
        # Function information
        # -------------------------

        typer.echo(
            f"Function: "
            f"{result['function']}"
        )

        typer.echo(
            f"Parameters: "
            f"{', '.join(result['parameters'])}"
        )

        typer.echo(
            f"Return expression: "
            f"{result['return_expression']}"
        )

        typer.echo(
            f"Operation: "
            f"{result['operation']}"
        )

        # -------------------------
        # Inferred return type
        # -------------------------

        typer.echo(
            f"Inferred return type: "
            f"{result['inferred_type']} "
            f"(confidence: "
            f"{result['confidence']})"
        )

        # -------------------------
        # Evidence
        # -------------------------

        typer.echo(
            f"Evidence: "
            f"{result['evidence']}"
        )

        # -------------------------
        # Migration suggestions
        # -------------------------

        if result["suggestions"]:

            typer.echo(
                "\nMigration Suggestions:"
            )

            for suggestion in result["suggestions"]:

                typer.echo(
                    f"  {suggestion['name']} → "
                    f"{suggestion['type']} "
                    f"(confidence: "
                    f"{suggestion['confidence']})"
                )

            typer.echo(
                f"  return → "
                f"{result['inferred_type']} "
                f"(confidence: "
                f"{result['confidence']})"
            )

        typer.echo(
            "────────────────────────"
        )

    # -------------------------
    # TypeScript transformation
    # -------------------------

    transformed_code = (
        transform_to_typescript(
            source_code,
            results,
        )
    )

    # -------------------------
    # TypeScript validation
    # -------------------------

    validation = validate_typescript(
        transformed_code
    )

    typer.echo(
        "\nValidation:"
    )

    typer.echo(
        "────────────────────────"
    )

    if validation["valid"]:

        typer.echo(
            "✓ Generated TypeScript "
            "is syntactically valid."
        )

    else:

        typer.echo(
            "✗ Generated TypeScript "
            "contains syntax errors."
        )

        for error in validation["errors"]:

            typer.echo(
                f"  - {error}"
            )

    typer.echo(
        "────────────────────────"
    )

    # -------------------------
    # TypeScript output
    # -------------------------

    typer.echo(
        "\nTypeScript Output:"
    )

    typer.echo(
        "────────────────────────"
    )

    typer.echo(
        transformed_code
    )

    typer.echo(
        "────────────────────────"
    )

    # -------------------------
    # Write output file
    # -------------------------

    if output:

        try:

            with open(
                output,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(
                    transformed_code
                )

            typer.echo(
                f"\n✓ TypeScript file created: "
                f"{output}"
            )

        except OSError as error:

            typer.echo(
                f"\nError writing output file: "
                f"{error}"
            )

            raise typer.Exit(
                code=1
            )


if __name__ == "__main__":
    app()