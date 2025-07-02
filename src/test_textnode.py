import unittest

# Assuming textnode.py contains the TextNode and TextType classes
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    # --- Equality Tests (__eq__) ---

    def test_eq_identical_nodes(self):
        """Tests that two identical nodes are considered equal."""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_identical_nodes_with_url(self):
        """Tests that two identical nodes with URLs are considered equal."""
        node = TextNode("This is a text node", TextType.LINK, "https://wikipedia.org")
        node2 = TextNode("This is a text node", TextType.LINK, "https://wikipedia.org")
        self.assertEqual(node, node2)

    def test_neq_different_text(self):
        """Tests that nodes with different text are not equal."""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node 2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_different_type(self):
        """Tests that nodes with different TextType are not equal."""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_neq_different_url(self):
        """Tests that nodes with different URLs are not equal."""
        # Comparing a node with a URL to one without
        node = TextNode("A node", TextType.LINK, url="https://a.com")
        node2 = TextNode("A node", TextType.LINK, url=None)
        self.assertNotEqual(node, node2)

        # Comparing two nodes with different URLs
        node3 = TextNode("A node", TextType.LINK, url="https://a.com")
        node4 = TextNode("A node", TextType.LINK, url="https://b.com")
        self.assertNotEqual(node3, node4)

    # --- Initialization and Representation Tests ---

    def test_init_attributes(self):
        """Tests that attributes are correctly set during initialization."""
        text = "A node"
        text_type = TextType.CODE
        url = "https://example.com"
        node = TextNode(text, text_type, url)
        self.assertEqual(node.text, text)
        self.assertEqual(node.text_type, text_type)
        self.assertEqual(node.url, url)

    def test_init_default_url(self):
        """Tests that the URL defaults to None if not provided."""
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)

    def test_repr(self):
        """Tests the __repr__ method for correct string formatting."""
        # Case 1: Node with a URL
        node_with_url = TextNode("A Link", TextType.LINK, "https://boot.dev")
        expected_repr_with_url = "TextNode(A Link, link, https://boot.dev)"
        self.assertEqual(repr(node_with_url), expected_repr_with_url)

        # Case 2: Node without a URL
        node_no_url = TextNode("Just text", TextType.PLAIN, None)
        expected_repr_no_url = "TextNode(Just text, plain, None)"
        self.assertEqual(repr(node_no_url), expected_repr_no_url)


if __name__ == "__main__":
    unittest.main()