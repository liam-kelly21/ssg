import unittest

from leafnode import LeafNode
from parentnode import ParentNode
from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()