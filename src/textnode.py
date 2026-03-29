from enum import Enum
from leafnode import LeafNode

class TextTypes(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextTypes.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextTypes.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextTypes.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextTypes.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextTypes.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextTypes.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unknown text type: {text_node.text_type}")

class TextNode:

    def __init__(self, text:str=None, text_type: TextTypes=TextTypes.TEXT, url:str=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if(
            self.text == other.text and
            self.text_type.value == other.text_type.value and
            self.url == other.url
            ):
            return True
        else:
            return False
    def __repr__(self):
        return f"TextNode(\"{self.text}\", {self.text_type}, \"{self.url}\")"


