from codeshift.parser.javascript import (
    parse_javascript,
)


def test_javascript_parser():

    source_code = """
    function add(a, b) {
        return a + b;
    }
    """

    tree = parse_javascript(
        source_code
    )

    assert tree.root_node.type == "program"

    assert (
        tree.root_node.named_child_count
        == 1
    )