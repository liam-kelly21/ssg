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

def markdown_to_html_node(markdown):
    html_nodes = []
    for block in markdown_to_blocks(markdown):
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                #inline formatting
                block = block.replace('\n', ' ')
                children = text_to_children(block)
                #apply tag
                html_nodes.append(ParentNode("p",children))
            case BlockType.HEADING:
                #strip
                block = block.replace('\n', ' ')
                count = len(re.match(r'^#+', block).group(0))
                head_text = block.lstrip("# ")
                #inline formatting
                children = text_to_children(head_text)
                #apply tag
                html_nodes.append(ParentNode(f"h{count}",children))
            case BlockType.CODE:
                #strip
                block = block.strip("`")
                block = block.lstrip("\n")
                #apply tags
                code_text = LeafNode("code",block)
                html_nodes.append(ParentNode("pre",[code_text]))
            case BlockType.QUOTE:
                #strip
                quote_text = ("".join(striplines(block,1))).strip()
                #inline formatting
                children = text_to_children(quote_text)
                html_nodes.append(ParentNode("blockquote",children))
            case BlockType.UNORDERED_LIST:
                #strip
                ul_text = striplines(block,2)
                #apply tags
                children = []
                for line in ul_text:
                    sub_children = text_to_children(line)
                    children.append(ParentNode("li",sub_children))
                html_nodes.append(ParentNode("ul",children))
            case BlockType.ORDERED_LIST:
                #strip
                ol_text = striplines(block,3)
                #apply tags
                children = []
                for line in ol_text:
                    sub_children = text_to_children(line)
                    children.append(ParentNode("li",sub_children))
                html_nodes.append(ParentNode("ol",children))
            case _:
                raise Exception("Incorrect block type")
            
    return ParentNode("div",html_nodes)

def striplines(text,chars):
    lines = text.splitlines(keepends=False)
    modified_lines = []
    for line in lines:
        modified_lines.append(line[chars:])
    return modified_lines

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def extract_title(md):
    if re.search(r"^# ",md):
        return md.splitlines()[0].lstrip("#").strip()
    else:
        raise Exception("Markdown does not begin with a title")

#helper functions created due to assignment structure - used in test cases, but unused in actual functionality
def split_nodes_image(old_nodes):
    return split_nodes_regex(old_nodes,IMAGES_PATTERN,TextType.IMAGE)

def split_nodes_link(old_nodes):
    return split_nodes_regex(old_nodes,LINKS_PATTERN,TextType.LINK)

def extract_markdown_links(text):
    return re.findall(LINKS_PATTERN,text)

def extract_markdown_images(text):
    return re.findall(IMAGES_PATTERN,text)