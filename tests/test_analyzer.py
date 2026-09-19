from codeshift.parser.javascript import (
    parse_javascript,
)

from codeshift.analyzer.javascript import (
    analyze_javascript,
)


def test_function_analysis():

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

    assert len(results) == 1

    result = results[0]

    assert result["function"] == "add"

    assert result["parameters"] == [
        "a",
        "b",
    ]

    assert (
        result["inferred_type"]
        == "number"
    )

    assert (
        result["confidence"]
        == "medium"
    )


def test_comparison_analysis():

    source_code = """
    function isAdult(age) {
        return age >= 18;
    }
    """

    tree = parse_javascript(
        source_code
    )

    results = analyze_javascript(
        tree
    )

    result = results[0]

    assert (
        result["inferred_type"]
        == "boolean"
    )

    assert (
        result["confidence"]
        == "high"
    )

    assert result["suggestions"][0][
        "type"
    ] == "number"


def test_numeric_literal_addition():

    source_code = """
    function addTen(a) {
        return a + 10;
    }
    """

    tree = parse_javascript(
        source_code
    )

    results = analyze_javascript(
        tree
    )

    result = results[0]

    assert (
        result["inferred_type"]
        == "number"
    )

    assert (
        result["confidence"]
        == "high"
    )

    assert (
        result["suggestions"][0]["name"]
        == "a"
    )

    assert (
        result["suggestions"][0]["type"]
        == "number"
    )

    assert (
        result["suggestions"][0]["confidence"]
        == "high"
    )


def test_multiply_by_number():

    source_code = """
    function multiplyByTwo(x) {
        return x * 2;
    }
    """

    tree = parse_javascript(
        source_code
    )

    results = analyze_javascript(
        tree
    )

    result = results[0]

    assert (
        result["inferred_type"]
        == "number"
    )

    assert (
        result["suggestions"][0]["type"]
        == "number"
    )

    assert (
        result["suggestions"][0]["confidence"]
        == "high"
    )


def test_string_concatenation():

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

    result = results[0]

    assert (
        result["inferred_type"]
        == "string"
    )

    assert (
        result["suggestions"][0]["name"]
        == "name"
    )

    assert (
        result["suggestions"][0]["type"]
        == "string"
    )

    assert (
        result["suggestions"][0]["confidence"]
        == "high"
    )

def test_nested_numeric_expression():

    source_code = """
    function calculate(a, b) {
        return (a + 10) * b;
    }
    """

    tree = parse_javascript(
        source_code
    )

    results = analyze_javascript(
        tree
    )

    result = results[0]

    assert (
        result["inferred_type"]
        == "number"
    )

    assert (
        result["confidence"]
        == "high"
    )

    suggestions = {
        item["name"]: item
        for item in result["suggestions"]
    }

    assert (
        suggestions["a"]["type"]
        == "number"
    )

    assert (
        suggestions["b"]["type"]
        == "number"
    )

    assert (
        suggestions["a"]["confidence"]
        == "high"
    )

    assert (
        suggestions["b"]["confidence"]
        == "high"
    )
