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

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches
    
# text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
# extract_markdown_images(text)
 
 #TODO   
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        matches = re.findall(r"(.*?)(!\[.*?\]\(.*?\))(.*?)|(.*)", node.text)
        for match in matches:
            # print(match)
            for string in match:
                if string == "":
                    continue
                if "![" in string:
                    img_tuple = extract_markdown_images(string)
                    if img_tuple:
                        alt_text, url = img_tuple[0]
                        new_nodes.append(TextNode(alt_text, TextTypes.IMAGE, url))
                else:
                    new_nodes.append(TextNode(string, TextTypes.TEXT))

    return new_nodes
        



#TODO
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        matches = re.findall(r"(.*?)(\[.*?\]\(.*?\))(.*?)|(.*)", node.text)
        for match in matches:
            # print(match)
            for string in match:
                if string == "":
                    continue
                if "[" in string and "](" in string:
                    img_tuple = extract_markdown_links(string)
                    if img_tuple:
                        alt_text, url = img_tuple[0]
                        new_nodes.append(TextNode(alt_text, TextTypes.LINK, url))
                else:
                    new_nodes.append(TextNode(string, TextTypes.TEXT))

    return new_nodes


# node = TextNode(
#     "This is text with a link ![to boot dev](https://www.boot.dev) and another ![to youtube](https://www.youtube.com/@bootdotdev), But that's the end",
#     TextTypes.TEXT,
# )

# new_nodes = split_nodes_links([node])