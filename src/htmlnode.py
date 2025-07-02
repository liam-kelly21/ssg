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