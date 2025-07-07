from nodes import *
import re
from enum import Enum

LINKS_PATTERN = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
IMAGES_PATTERN = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.PLAIN: 
            return LeafNode(None,text_node.text)
        case TextType.BOLD:
            return LeafNode("b",text_node.text)
        case TextType.ITALIC:
            return LeafNode("i",text_node.text)
        case TextType.CODE:
            return LeafNode("code",text_node.text)
        case TextType.LINK:
            return LeafNode("a",text_node.text,{"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img",None,{"src":text_node.url,"alt":text_node.text})
        case _:
            raise Exception("Invalid text type")

def split_nodes_delimeter(old_nodes, delimeter, text_type):
    new_nodes = []
    for node in old_nodes:
        first_delimeter = node.text.find(delimeter)
        if node.text_type != TextType.PLAIN or first_delimeter == -1:
            new_nodes.append(node)
            continue
        if node.text.count(delimeter) % 2:
            raise Exception("Invalid markdown syntax: Closing delimeter not found")
        
        node_is_delimeted = True
        if first_delimeter:
            node_is_delimeted = False
        node.text = node.text.rstrip(delimeter)
        node.text = node.text.lstrip(delimeter)
        
        for text_chunk in node.text.split(sep=delimeter):
            if node_is_delimeted:
                new_node = TextNode(text_chunk,text_type)
            else:
                new_node = TextNode(text_chunk,TextType.PLAIN)
            node_is_delimeted = not node_is_delimeted
            new_nodes.append(new_node)
        
    return new_nodes

def split_nodes_regex(old_nodes,pattern,text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        last_pos = 0
        chunk_pattern = re.compile(pattern)
        for match in chunk_pattern.finditer(node.text):
            start,end = match.span()
            if start > last_pos:
                new_nodes.append(TextNode(node.text[last_pos:start],TextType.PLAIN))
            new_nodes.append(TextNode(match[1],text_type,match[2]))
            last_pos = end
        if last_pos < len(node.text):
            new_nodes.append(TextNode(node.text[last_pos:],TextType.PLAIN))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text,TextType.PLAIN)]
    nodes = split_nodes_delimeter(nodes,"**",TextType.BOLD)
    nodes = split_nodes_delimeter(nodes,"_",TextType.ITALIC)
    nodes = split_nodes_delimeter(nodes,"`",TextType.CODE)
    nodes = split_nodes_regex(nodes,IMAGES_PATTERN,TextType.IMAGE)
    nodes = split_nodes_regex(nodes,LINKS_PATTERN,TextType.LINK)
    return nodes

def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    lines = map(lambda x:x.strip(),lines)
    lines = list(filter(None,lines))
    return lines

def block_to_block_type(block):
    if re.search(r"^#{1,6} ",block):
        return BlockType.HEADING
    elif block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    
    lines = block.split("\n")
    quote = True
    ul = True
    ol = True
    count = 0
    for line in lines:
        count += 1
        if not line:
            quote = False
            ul = False
            ol = False
            break
        if line[0] != ">":
            quote = False
        if line[0:2] != "- ":
            ul = False
        if line[0:3] != f"{count}. ":
            ol = False
    
    if quote:
        return BlockType.QUOTE
    if ul:
        return BlockType.UNORDERED_LIST
    if ol:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH


'''Create a new function called def markdown_to_html_node(markdown): that converts a full markdown document into a single parent HTMLNode. That one parent HTMLNode should (obviously) contain many child HTMLNode objects representing the nested elements.

FYI: I created an additional 8 helper functions to keep my code neat and easy to understand, because there's a lot of logic necessary for markdown_to_html_node. I don't want to give you my exact functions because I want you to do this from scratch. However, I'll give you the basic order of operations:

    Split the markdown into blocks (you already have a function for this)
    Loop over each block:
        Determine the type of block (you already have a function for this)
        Based on the type of block, create a new HTMLNode with the proper data
        Assign the proper child HTMLNode objects to the block node. I created a shared text_to_children(text) function that works for all block types. It takes a string of text and returns a list of HTMLNodes that represent the inline markdown using previously created functions (think TextNode -> HTMLNode).
        The "code" block is a bit of a special case: it should not do any inline markdown parsing of its children. I didn't use my text_to_children function for this block type, I manually made a TextNode and used text_node_to_html_node.
    Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.'''

def markdown_to_html_node(markdown):
    html_nodes = []
    for block in markdown_to_blocks(markdown):
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                html_nodes.append(LeafNode("p",block))
                #this might have bold/italics nested tho
            case BlockType.HEADING:
                count = len(re.match(r'^#+', block).group(0))
                head_text = block.lstrip("# ")
                html_nodes.append(LeafNode(f"h{count}",head_text))
            case BlockType.CODE:
                block = block.strip("`")
                code_text = LeafNode("code",block)
                html_nodes.append(ParentNode("pre",code_text))
            case BlockType.QUOTE:
                lines = block.splitlines(keepends=True) # keepends preserves newline chars
                modified_lines = []
                for line in lines:
                    if line.startswith(">"):
                        modified_lines.append(line[1:])
                    else:
                        modified_lines.append(line)
                quote_text = "".join(modified_lines)
                html_nodes.append(LeafNode("blockquote",quote_text))
            case BlockType.UNORDERED_LIST:
                pass
            case BlockType.ORDERED_LIST:
                pass
            case _:
                raise Exception("Incorrect block type")
            
    return ParentNode("div",html_nodes)

# take text
# return 

'''
create a 
text to textnodes -> textnode to htmlnode can take raw text and produce HTML leaf nodes.

PARAGRAPH = "paragraph"
HEADING = "heading"
CODE = "code"
QUOTE = "quote"
UNORDERED_LIST = "unordered_list"
ORDERED_LIST = "ordered_list"


Quote blocks should be surrounded by a <blockquote> tag.
Unordered list blocks should be surrounded by a <ul> tag, and each list item should be surrounded by a <li> tag.
Ordered list blocks should be surrounded by a <ol> tag, and each list item should be surrounded by a <li> tag.
Code blocks should be surrounded by a <code> tag nested inside a <pre> tag.
Headings should be surrounded by a <h1> to <h6> tag, depending on the number of # characters.
Paragraphs should be surrounded by a <p> tag.
'''
    

#helper functions created due to assignment structure - used in test cases, but unused in actual functionality
def split_nodes_image(old_nodes):
    return split_nodes_regex(old_nodes,IMAGES_PATTERN,TextType.IMAGE)

def split_nodes_link(old_nodes):
    return split_nodes_regex(old_nodes,LINKS_PATTERN,TextType.LINK)

def extract_markdown_links(text):
    return re.findall(LINKS_PATTERN,text)

def extract_markdown_images(text):
    return re.findall(IMAGES_PATTERN,text)