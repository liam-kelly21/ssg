import unittest

from leafnode import LeafNode

class TestTextNode(unittest.TestCase):
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