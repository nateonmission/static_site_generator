

class HTMLNode:
    def __init__(self, tag=None, children=None, value=None, props=None):
        self.tag = tag
        self.children = children
        self.value = value
        self.props = props
        
    def to_html(self):
        raise NotImplementedError("to_html method must be implemented by subclasses")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        else:
            return " " + " ".join([f'{key}="{value}"' for key, value in self.props.items()])
        
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, children={self.children}, value={self.value}, props={self.props})"
           
        
        
        