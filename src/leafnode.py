from htmlnode import *

class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(self,tag,value,None,props)
    
    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return str(self.value)
        properties = ""
        for prop in self.props:
            properties += f" {prop}=\"{self.props[prop]}\""
        return f"<{self.tag}{properties}>{self.value}</{self.tag}>"