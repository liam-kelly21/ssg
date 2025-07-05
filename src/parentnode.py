from htmlnode import *

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
        