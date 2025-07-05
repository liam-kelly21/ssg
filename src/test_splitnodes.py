import unittest
from splitnodes import split_nodes_delimeter
from textnode import *

'''
To test:
- italics and code
- mixture of delimeters
- nodes that are not texttype plain
- nodes that are not texttype plain but contain the delimeter we're looking for
- nodes that have an unbalanced delimeter
- a delimited section ending a string
'''

class TestSplitNode(unittest.TestCase):
    def test_split_bf(self):
        old_nodes = [
            TextNode("This is some test **bolded** text",TextType.PLAIN),
            TextNode("**This is some more** test bolded text",TextType.PLAIN),
            TextNode("This is **some** final **bolded text** for testing",TextType.PLAIN)
            ]
        result = split_nodes_delimeter(old_nodes,"**",TextType.BOLD)
        expected_result = [
            TextNode("This is some test ",TextType.PLAIN),
            TextNode("bolded",TextType.BOLD),
            TextNode(" text",TextType.PLAIN),
            TextNode("This is some more",TextType.BOLD),
            TextNode(" test bolded text",TextType.PLAIN),
            TextNode("This is ",TextType.PLAIN),
            TextNode("some",TextType.BOLD),
            TextNode(" final ",TextType.PLAIN),
            TextNode("bolded text",TextType.BOLD),
            TextNode(" for testing",TextType.PLAIN)
        ]
        self.assertEqual(result,expected_result)
    
    def test_split_it(self):
        result = split_nodes_delimeter([TextNode("This is some text _ending in italics_",TextType.PLAIN),],"_",TextType.ITALIC)
        expected_result = [
            TextNode("This is some text ",TextType)
        ]


if __name__ == "__main__":
    unittest.main()