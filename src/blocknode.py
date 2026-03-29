from enum import Enum
import re

# from textprocessing import markdown_to_html

class BlockTypes(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
    
def block_to_block_type(block):
    heading = re.match(r"^#+ ", block)
    if heading:
        return BlockTypes.HEADING
    elif block.startswith("```"):
        return BlockTypes.CODE
    elif block.startswith("> "):
        return BlockTypes.QUOTE
    elif block.startswith("- "):
        return BlockTypes.UNORDERED_LIST
    elif block[0].isdigit() and ". " in block[1:5]:
        return BlockTypes.ORDERED_LIST
    else:
        return BlockTypes.PARAGRAPH
    
    

# class BlockNode:

#     def __init__(self, text:str=None, text_type: TextTypes=TextTypes.TEXT, url:str=None):
#         self.text = text
#         self.text_type = text_type
#         self.url = url

#     def __eq__(self, other):
#         if(
#             self.text == other.text and
#             self.text_type.value == other.text_type.value and
#             self.url == other.url
#             ):
#             return True
#         else:
#             return False
#     def __repr__(self):
#         return f"TextNode(\"{self.text}\", {self.text_type}, \"{self.url}\")"