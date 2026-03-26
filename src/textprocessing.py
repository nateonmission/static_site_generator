import re

from textnode import TextNode, TextTypes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextTypes.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError(f"Missing closing delimiter: {delimiter}")

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextTypes.TEXT))
            else:
                match delimiter:
                    case "**":
                        new_nodes.append(TextNode(part, TextTypes.BOLD))
                    case "*":
                        new_nodes.append(TextNode(part, TextTypes.ITALIC))
                    case "`":
                        new_nodes.append(TextNode(part, TextTypes.CODE))
                    case _:
                        raise ValueError(f"Unknown delimiter: {delimiter}")

    return new_nodes
            
            
def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches
    
# text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
# extract_markdown_images(text)
    