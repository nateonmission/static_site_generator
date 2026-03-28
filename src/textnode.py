from enum import Enum

class TextTypes(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

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


