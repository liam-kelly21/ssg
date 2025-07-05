from textnode import *

def split_nodes_delimeter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        first_delimeter = node.text.find(delimiter)
        if node.text_type != TextType.PLAIN or first_delimeter == -1:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2:
            raise Exception("Invalid markdown syntax: Closing delimiter not found")
        
        node_is_delimeted = True
        if first_delimeter:
            node_is_delimeted = False
        
        for text_chunk in node.text.split(sep=delimiter):
            if node_is_delimeted:
                new_node = TextNode(text_chunk,text_type)
            else:
                new_node = TextNode(text_chunk,TextType.PLAIN)
            node_is_delimeted = not node_is_delimeted
            new_nodes.append(new_node)
        
        return new_nodes