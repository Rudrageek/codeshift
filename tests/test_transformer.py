from codeshift.parser.javascript import (
    parse_javascript,
)

from codeshift.analyzer.javascript import (
    analyze_javascript,
)

from codeshift.transformer.typescript import (
    transform_to_typescript,
)


def test_numeric_transformation():
    source_code = """
function multiply(a, b) {
    return a * b;
}
"""

    tree = parse_javascript(
        source_code
    )

    results = analyze_javascript(
        tree
    )

    transformed = transform_to_typescript(
        source_code,
        results,
    )

    assert (
        "function multiply(a: number, b: number): number"
        in transformed
    )

    assert (
        "return a * b;"
        in transformed
    )


def test_string_transformation():
    source_code = """
function greet(name) {
    return "Hello " + name;
}
"""

    tree = parse_javascript(
        source_code
    )

    results = analyze_javascript(
        tree
    )

    transformed = transform_to_typescript(
        source_code,
        results,
    )

    assert (
        "function greet(name: string): string"
        in transformed
    )


def test_medium_confidence_warning():
    source_code = """
function add(a, b) {
    return a + b;
}
"""

    tree = parse_javascript(
        source_code
    )

    results = analyze_javascript(
        tree
    )

    transformed = transform_to_typescript(
        source_code,
        results,
    )

    assert (
        "a: number"
        in transformed
    )

    assert (
        "b: number"
        in transformed
    )

    assert (
        "CodeShift warning"
        in transformed
    )