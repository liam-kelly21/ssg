from enum import Enum

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self,text,text_type,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self,other):
        if (self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

class HTMLNode():
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        attributes = ""
        if self.props is None:
            return None
        for attribute in self.props:
            attributes += (" " + attribute + "=\"" + self.props[attribute] + "\"")
        return attributes
    
    def __repr__(self):
        return f'''
        HTMLNode \n
        {self.tag} \n
        {self.value} \n
        {self.children} \n
        {self.props_to_html()}
        '''
    
class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag,None,children,props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Error: Missing tag")
        if not self.children:
            raise ValueError("Error: Missing children")
        childtext= ""
        for child in self.children:
            childtext += child.to_html()
        return f"<{self.tag}>{childtext}</{self.tag}>"
    
class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag,value,None,props)
    
    def to_html(self):
        if not self.value:
            self.value = ""
        if not self.tag:
            return str(self.value)
        properties = ""
        if self.props:
            for prop in self.props:
                properties += f" {prop}=\"{self.props[prop]}\""
        return f"<{self.tag}{properties}>{self.value}</{self.tag}>"