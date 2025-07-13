import unittest

# Assuming textnode.py contains the TextNode and TextType classes
from nodes import *

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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # Edge Case: ParentNode with no tag
    def test_to_html_no_tag(self):
        with self.assertRaisesRegex(ValueError, "Error: Missing tag"):
            parent_node = ParentNode(None, [LeafNode("p", "text")])
            parent_node.to_html()

    # Edge Case: ParentNode with no children
    def test_to_html_no_children(self):
        with self.assertRaisesRegex(ValueError, "Error: Missing children"):
            parent_node = ParentNode("div", [])
            parent_node.to_html()
            
    # Edge Case: ParentNode with mixed children (LeafNode and other ParentNode)
    def test_to_html_mixed_children(self):
        child1 = LeafNode("p", "paragraph")
        child2 = ParentNode("section", [LeafNode("h1", "Heading")])
        parent_node = ParentNode("article", [child1, child2])
        expected_html = "<article><p>paragraph</p><section><h1>Heading</h1></section></article>"
        self.assertEqual(parent_node.to_html(), expected_html)

    # Edge Case: ParentNode with multiple levels of nesting
    def test_to_html_deep_nesting(self):
        node1 = LeafNode("a", "Link", {"href": "url.com"})
        node2 = ParentNode("li", [LeafNode("code", "print('hello')")])
        node3 = LeafNode("em", "emphasized text")
        
        child_list = ParentNode("ul", [node2, LeafNode("li", "Another item")])
        
        main_div = ParentNode("div", [
            LeafNode("h1", "Title"),
            ParentNode("p", [node1, node3]),
            child_list
        ])
        
        expected_html = (
            "<div>"
            "<h1>Title</h1>"
            "<p><a href=\"url.com\">Link</a><em>emphasized text</em></p>"
            "<ul><li><code>print('hello')</code></li><li>Another item</li></ul>"
            "</div>"
        )
        self.assertEqual(main_div.to_html(), expected_html)

    # Edge Case: ParentNode with children that have props
    def test_to_html_children_with_props(self):
        child_node = LeafNode("img", "Here's an image", {"src": "image.jpg", "alt": "A picture"})
        parent_node = ParentNode("figure", [child_node])
        expected_html = "<figure><img src=\"image.jpg\" alt=\"A picture\">Here's an image</img></figure>"
        self.assertEqual(parent_node.to_html(), expected_html)

    # Edge Case: ParentNode with props
    def test_to_html_with_props(self):
        child_node = LeafNode("p", "Content")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        # Note: Current to_html doesn't render props for ParentNode itself.
        # This test ensures it still processes children correctly.
        expected_html = "<div><p>Content</p></div>" 
        self.assertEqual(parent_node.to_html(), expected_html)
    
    # Edge Case: ParentNode with a text node as a child (not explicitly handled by ParentNode init)
    def test_to_html_with_text_child(self):
        # This implies HTMLNode supports text directly, but the current ParentNode
        # expects HTMLNode objects in its children list.
        # Assuming TextNode is a type of LeafNode for this context, or it's implicitly
        # handled by LeafNode if a tag is omitted.
        text_node = LeafNode(None, "Just some text")
        parent_node = ParentNode("p", [text_node])
        self.assertEqual(parent_node.to_html(), "<p>Just some text</p>")

    # Edge Case: ParentNode with only one child
    def test_to_html_single_child(self):
        child_node = LeafNode("strong", "Important")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><strong>Important</strong></div>")

    # Edge Case: ParentNode where a child's to_html method itself raises an error
    def test_to_html_child_error_propagation(self):
        class MalformedChild(HTMLNode):
            def to_html(self):
                raise ValueError("Bad child node")
        
        parent_node = ParentNode("div", [MalformedChild(None, None, None, None)])
        with self.assertRaisesRegex(ValueError, "Bad child node"):
            parent_node.to_html()

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_href(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(),"<a href=\"https://www.google.com\">Click me!</a>")
    
    def test_leaf_children(self):
        node = LeafNode("p","Content")
        self.assertEqual(node.children,None)
    
    def test_leaf_to_html_error(self):
        node = LeafNode("p",None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_return_plain_value(self):
        node = LeafNode(None,"This is test content", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(),"This is test content")
    
    def test_multiple_props(self):
        node = LeafNode("a","Hello world!",{"href": "https://www.google.com","test":"test value"})
        self.assertEqual(node.to_html(),"<a href=\"https://www.google.com\" test=\"test value\">Hello world!</a>")

if __name__ == "__main__":
    unittest.main()