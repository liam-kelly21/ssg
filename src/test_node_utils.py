import unittest
from node_utils import *
from nodes import TextNode,TextType

class TestSplitNode(unittest.TestCase):
    def test_split_bf(self):
        self.maxDiff = None
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
        result = split_nodes_delimeter([TextNode("This is some text _ending in italics_",TextType.PLAIN)],"_",TextType.ITALIC)
        expected_result = [
            TextNode("This is some text ",TextType.PLAIN),
            TextNode("ending in italics",TextType.ITALIC)
        ]
        self.assertEqual(result,expected_result)
    
    def test_split_code(self):
        result = split_nodes_delimeter([TextNode("This is some text `ending in code`",TextType.PLAIN)],"`",TextType.CODE)
        expected_result = [
            TextNode("This is some text ",TextType.PLAIN),
            TextNode("ending in code",TextType.CODE)
        ]
        self.assertEqual(result,expected_result)

    def test_split_mixed(self):
        result = split_nodes_delimeter([TextNode("This is some text _ending in italics **with a bold section in the middle** that shouldn't be detected_",TextType.PLAIN)],"_",TextType.ITALIC)
        expected_result = [
            TextNode("This is some text ",TextType.PLAIN),
            TextNode("ending in italics **with a bold section in the middle** that shouldn't be detected",TextType.ITALIC)
        ]
        self.assertEqual(result,expected_result)

    def test_split_nonplain(self):
        result = split_nodes_delimeter([TextNode("This is some text _ending in italics_",TextType.LINK,"google.com")],"_",TextType.ITALIC)
        expected_result = [
            TextNode("This is some text _ending in italics_",TextType.LINK,"google.com")
        ]
        self.assertEqual(result,expected_result)

    def test_split_unbalanced(self):
        with self.assertRaisesRegex(Exception, "Invalid markdown syntax: Closing delimeter not found"):
            split_nodes_delimeter([TextNode("This is some text _ending in italics",TextType.PLAIN)],"_",TextType.ITALIC)

class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href":"google.com"})
        self.assertEqual(html_node.value, "This is a text node")

    def test_img(self):
        node = TextNode("This is a text node", TextType.IMAGE, "google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src":"google.com","alt":"This is a text node"})
        self.assertEqual(html_node.value, None)
    
    def test_error(self):
        with self.assertRaisesRegex(Exception,"Invalid text type"):
            node = TextNode("This is a text node",3)
            text_node_to_html_node(node)

class TestMarkdownExtraction(unittest.TestCase):

    def test_no_matches(self):
        """Test strings that contain no valid markdown links or images."""
        self.assertListEqual(extract_markdown_images("This string has no images."), [])
        self.assertListEqual(extract_markdown_links("This string has no links."), [])
        self.assertListEqual(extract_markdown_images(""), [])
        self.assertListEqual(extract_markdown_links(""), [])

    def test_extract_single_image(self):
        """Test a basic string with one image."""
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_single_link(self):
        """Test a basic string with one link."""
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)

    def test_extract_multiple_items(self):
        """Test that multiple, distinct items in a string are all found."""
        text = "![image1](url1.png) and ![image2](url2.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image1", "url1.png"), ("image2", "url2.png")], matches)

        text = "[link1](url1.html) and [link2](url2.html)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link1", "url1.html"), ("link2", "url2.html")], matches)

    def test_mixed_content(self):
        """Test that images are not extracted as links, and vice versa."""
        text = "This is a [link](link.html) and this is an ![image](image.png)."
        
        image_matches = extract_markdown_images(text)
        self.assertListEqual([("image", "image.png")], image_matches)

        link_matches = extract_markdown_links(text)
        self.assertListEqual([("link", "link.html")], link_matches)

    def test_incorrect_syntax(self):
        """Test various forms of incorrect or incomplete syntax that should not match."""
        self.assertListEqual(extract_markdown_images("![missing url]()"), [("missing url", "")]) # empty url is valid
        self.assertListEqual(extract_markdown_images("![](missing_alt.png)"), [("", "missing_alt.png")]) # empty alt is valid
        self.assertListEqual(extract_markdown_links("[missing url]()"), [("missing url", "")]) # empty url is valid
        self.assertListEqual(extract_markdown_links("[] (missing_text.com)"), []) # missing text is invalid for links
        self.assertListEqual(extract_markdown_links("[text] (no_parentheses.com)"), [])
        self.assertListEqual(extract_markdown_images("![text] (no_parentheses.com)"), [])
        self.assertListEqual(extract_markdown_links("text](malformed.com)"), [])
        self.assertListEqual(extract_markdown_images("!image](malformed.com)"), [])

    def test_adjacent_items(self):
        """Test items that are immediately next to each other."""
        text = "![img1](url1)![img2](url2)[link1](url3)[link2](url4)"
        
        image_matches = extract_markdown_images(text)
        self.assertListEqual([("img1", "url1"), ("img2", "url2")], image_matches)

        link_matches = extract_markdown_links(text)
        self.assertListEqual([("link1", "url3"), ("link2", "url4")], link_matches)

class TestSplitNodesImagesAndLinks(unittest.TestCase):
    '''
    Things to test
    - mix of images and links
    - starting with an image
    '''

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_no_links(self):
        node = TextNode(
            "This is text with no links",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no links", TextType.PLAIN)
            ],
            new_nodes,
        )

    def test_split_images_many_nodes(self):
        node1 = TextNode(
            "This is a first sequence of text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        node2 = TextNode(
            "This is a second sequence of text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        node3 = TextNode(
            "This is a third sequence of text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node1,node2,node3])
        self.assertListEqual(
            [
                TextNode("This is a first sequence of text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is a second sequence of text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is a third sequence of text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_no_text(self):
        node = TextNode(
            "",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
            ],
            new_nodes,
        )

    def test_split_first_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) Look at this image.",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" Look at this image.", TextType.PLAIN)
            ],
            new_nodes,
        )

    def test_split_mixed(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) Look at this image. [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" Look at this image. [link](https://i.imgur.com/zjjcJKZ.png)", TextType.PLAIN)
            ],
            new_nodes,
        )
    
class TestTextToTextNodes(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_multi_items(self):
        """ The original test case for a mixed, well-formed string. """
        new_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_only_plain_text(self):
        """ Tests that a string with no special syntax returns a single plain text node. """
        new_nodes = text_to_textnodes("This is a plain sentence.")
        self.assertListEqual(
            [TextNode("This is a plain sentence.", TextType.PLAIN)],
            new_nodes
        )

    def test_starts_and_ends_with_markdown(self):
        """ Tests strings that begin and end with formatted elements, with no surrounding plain text. """
        new_nodes = text_to_textnodes("**Start bold** and _end italic_")
        self.assertListEqual(
            [
                TextNode("Start bold", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("end italic", TextType.ITALIC),
            ],
            new_nodes
        )

    def test_consecutive_markdown(self):
        """ Tests multiple formatted elements directly adjacent to each other. """
        new_nodes = text_to_textnodes("One**two**`three`_four_")
        self.assertListEqual(
            [
                TextNode("One", TextType.PLAIN),
                TextNode("two", TextType.BOLD),
                TextNode("three", TextType.CODE),
                TextNode("four", TextType.ITALIC),
            ],
            new_nodes
        )

    def test_malformed_image_and_link(self):
        """ Tests malformed image/link syntax, which should be treated as plain text. """
        new_nodes = text_to_textnodes("This is a ![bad image]( and a [bad link](.")
        self.assertListEqual(
            [TextNode("This is a ![bad image]( and a [bad link](.", TextType.PLAIN)],
            new_nodes
        )

    def test_empty_string(self):
        """ Tests that an empty string input returns an empty list. """
        new_nodes = text_to_textnodes("")
        self.assertListEqual([], new_nodes)

    def test_whitespace_only(self):
        """ Tests that a string containing only whitespace returns a single plain text node. """
        new_nodes = text_to_textnodes("   \t\n ")
        self.assertListEqual(
            [TextNode("   \t\n ", TextType.PLAIN)],
            new_nodes
        )

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_types(self):
        testquote = '''>hi
>this is a test quote
>yay text!'''
        testul = '''- bananas
- milk
- eggs'''
        testol = '''1. item 1
2. item 2
3. item 3'''
        self.assertEqual(block_to_block_type("## Heading 2"),BlockType.HEADING)
        self.assertEqual(block_to_block_type("```Code```"),BlockType.CODE)
        self.assertEqual(block_to_block_type(testquote),BlockType.QUOTE)
        self.assertEqual(block_to_block_type(testul),BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(testol),BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("I'm just some text!"),BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()