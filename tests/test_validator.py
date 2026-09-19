from codeshift.validator.typescript import (
    validate_typescript,
)


def test_valid_typescript():

    source_code = """
    function add(
        a: number,
        b: number
    ): number {
        return a + b;
    }
    """

    result = validate_typescript(
        source_code
    )

    assert result["syntax_valid"] is True

    assert result["semantic_valid"] is True

    assert result["valid"] is True

    assert result["semantic_errors"] == []


def test_invalid_typescript():

    source_code = """
    function add(
        a: number,
        b: string
    ): number {
        return a + b;
    }
    """

    result = validate_typescript(
        source_code
    )

    assert result["syntax_valid"] is True

    assert result["semantic_valid"] is False

    assert result["valid"] is False

    assert len(
        result["semantic_errors"]
    ) > 0