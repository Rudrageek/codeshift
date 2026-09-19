import subprocess
import tempfile
from pathlib import Path


def validate_typescript_syntax(source_code: str) -> dict:
    """
    Validate TypeScript syntax using Tree-sitter.

    Returns:
        {
            "valid": bool,
            "errors": list[str]
        }
    """

    from tree_sitter import Language, Parser
    import tree_sitter_typescript

    typescript_language = Language(
        tree_sitter_typescript.language_typescript()
    )

    parser = Parser(
        typescript_language
    )

    tree = parser.parse(
        source_code.encode("utf-8")
    )

    root = tree.root_node

    errors = []

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

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }


def validate_typescript_semantics(
    source_code: str,
) -> dict:
    """
    Validate TypeScript using the TypeScript compiler (tsc).

    Performs semantic and type checking.

    Returns:
        {
            "valid": bool,
            "errors": list[str]
        }
    """

    temp_file = None

    try:

        # ---------------------------------
        # Create temporary TypeScript file
        # ---------------------------------

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".ts",
            delete=False,
            encoding="utf-8",
        ) as file:

            file.write(source_code)

            temp_file = Path(
                file.name
            )

        # ---------------------------------
        # Find npm global installation
        # ---------------------------------

        npm_prefix_result = subprocess.run(
            [
                "npm",
                "config",
                "get",
                "prefix",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        npm_prefix = (
            npm_prefix_result.stdout.strip()
        )

        tsc_path = (
            Path(npm_prefix)
            / "tsc.cmd"
        )

        # ---------------------------------
        # Check TypeScript compiler
        # ---------------------------------

        if not tsc_path.exists():

            return {
                "valid": False,
                "errors": [
                    "TypeScript compiler was not found at: "
                    f"{tsc_path}"
                ],
            }

        # ---------------------------------
        # Run TypeScript compiler
        # ---------------------------------

        result = subprocess.run(
            [
                str(tsc_path),
                str(temp_file),
                "--noEmit",
                "--strict",
                "--skipLibCheck",
            ],
            capture_output=True,
            text=True,
        )

        errors = []

        # ---------------------------------
        # Collect stdout errors
        # ---------------------------------

        if result.stdout.strip():

            errors.extend(
                line.strip()
                for line in result.stdout.splitlines()
                if line.strip()
            )

        # ---------------------------------
        # Collect stderr errors
        # ---------------------------------

        if result.stderr.strip():

            errors.extend(
                line.strip()
                for line in result.stderr.splitlines()
                if line.strip()
            )

        return {
            "valid": result.returncode == 0,
            "errors": errors,
        }

    except FileNotFoundError:

        return {
            "valid": False,
            "errors": [
                "npm was not found. "
                "Please make sure Node.js is installed."
            ],
        }

    except subprocess.CalledProcessError as error:

        return {
            "valid": False,
            "errors": [
                "Could not determine npm installation path.",
                str(error),
            ],
        }

    finally:

        # ---------------------------------
        # Remove temporary file
        # ---------------------------------

        if (
            temp_file
            and temp_file.exists()
        ):

            try:

                temp_file.unlink()

            except OSError:

                pass


def validate_typescript(
    source_code: str,
) -> dict:
    """
    Perform complete TypeScript validation.

    Validation layers:

    1. Tree-sitter syntax validation
    2. TypeScript compiler semantic validation
    """

    # ---------------------------------
    # Step 1: Syntax validation
    # ---------------------------------

    syntax_result = (
        validate_typescript_syntax(
            source_code
        )
    )

    if not syntax_result["valid"]:

        return {
            "valid": False,
            "syntax_valid": False,
            "semantic_valid": False,
            "syntax_errors": (
                syntax_result["errors"]
            ),
            "semantic_errors": [],
        }

    # ---------------------------------
    # Step 2: Semantic validation
    # ---------------------------------

    semantic_result = (
        validate_typescript_semantics(
            source_code
        )
    )

    return {
        "valid": semantic_result["valid"],
        "syntax_valid": True,
        "semantic_valid": (
            semantic_result["valid"]
        ),
        "syntax_errors": [],
        "semantic_errors": (
            semantic_result["errors"]
        ),
    }