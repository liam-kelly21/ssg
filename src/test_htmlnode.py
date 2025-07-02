import unittest

# Assuming the HTMLNode class is in a file named htmlnode.py
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    # --- Initialization Tests ---

    def test_init_all_none(self):
        """Tests initialization with all default (None) values."""
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_values(self):
        """Tests initialization with specific values for all properties."""
        tag = "p"
        value = "This is a paragraph."
        children = []
        props = {"class": "my-class"}
        node = HTMLNode(tag, value, children, props)
        self.assertEqual(node.tag, tag)
        self.assertEqual(node.value, value)
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    # --- props_to_html Method Tests ---

    def test_props_to_html_with_props(self):
        """Tests conversion of a props dictionary to an HTML attribute string."""
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode(props=props)
        expected_html = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_html)

    def test_props_to_html_empty(self):
        """Tests conversion with an empty props dictionary."""
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none(self):
        """Tests that props_to_html raises an error if props is None."""
        # The current implementation will raise a TypeError when trying to iterate
        # over None. A robust test should confirm this expected behavior.
        node = HTMLNode(props=None)
        with self.assertRaises(TypeError):
            node.props_to_html()

    # --- to_html Method Tests ---

    def test_to_html_raises_error(self):
        """Tests that the base to_html method raises NotImplementedError."""
        node = HTMLNode()
        # Use assertRaises to confirm that the expected exception is thrown.
        with self.assertRaises(NotImplementedError):
            node.to_html()

    # --- __repr__ Method Tests ---

    def test_repr(self):
        """Tests the __repr__ method for correct string formatting."""
        node = HTMLNode(
            tag="a",
            value="Click me!",
            children=None,
            props={"href": "https://www.boot.dev"}
        )
        # The expected string needs to match the multi-line format exactly
        expected_repr = '''
        HTMLNode \n
        a \n
        Click me! \n
        None \n
         href="https://www.boot.dev"
        '''
        self.assertEqual(repr(node), expected_repr)


if __name__ == "__main__":
    unittest.main()