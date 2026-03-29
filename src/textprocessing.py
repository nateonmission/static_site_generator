import re

from textnode import TextNode, TextTypes, text_node_to_html_node
from leafnode import LeafNode
from blocknode import BlockTypes, block_to_block_type

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
                    case "_":
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
                    new_nodes.append(TextNode(string, node.text_type, node.url ))

    return new_nodes
        



def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextTypes.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_links(text)

        if not matches:
            new_nodes.append(node)
            continue

        for anchor_text, url in matches:
            markdown = f"[{anchor_text}]({url})"
            before, after = text.split(markdown, 1)

            if before:
                new_nodes.append(TextNode(before, TextTypes.TEXT))

            new_nodes.append(TextNode(anchor_text, TextTypes.LINK, url))

            text = after  # keep processing the remainder

        if text:
            new_nodes.append(TextNode(text, TextTypes.TEXT))

    return new_nodes
    # new_nodes = []
    # for node in old_nodes:
    #     matches = re.findall(r"(.*?)(\[.*?\]\(.*?\))(.*?)|(.*)", node.text)
    #     for match in matches:
    #         # print(match)
    #         for string in match:
    #             if string == "":
    #                 continue
    #             if "[" in string and "](" in string:
    #                 img_tuple = extract_markdown_links(string)
    #                 if img_tuple:
    #                     alt_text, url = img_tuple[0]
    #                     new_nodes.append(TextNode(alt_text, TextTypes.LINK, url))
    #             else:
    #                 new_nodes.append(TextNode(string, node.text_type,node.url))
    # return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextTypes.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextTypes.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextTypes.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextTypes.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
    
    
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks if block.strip() != ""]
    return blocks

def blocks_to_BlockNodes(blocks_list):
    block_nodes = []
    for block in blocks_list:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockTypes.HEADING:
                heading_level = block.count("#", 0, block.find(" "))
                block_tag = f"h{heading_level}"
                block = block[heading_level+1:].strip()
            case BlockTypes.CODE:
                block_tag = "code"
            case BlockTypes.QUOTE:
                block_tag = "blockquote"
            case BlockTypes.UNORDERED_LIST:
                block_tag = "ul"
            case BlockTypes.ORDERED_LIST:
                block_tag = "ol"
            case BlockTypes.PARAGRAPH:
                block_tag = "p"
                block = " ".join(line.strip() for line in block.split("\n"))
            case _:
                raise ValueError(f"Unknown block type: {block_type}")
        if block_type in [BlockTypes.UNORDERED_LIST, BlockTypes.ORDERED_LIST]:  
            list_items = block.split("\n")
            list_items = [item.strip() for item in list_items if item.strip() != ""]
            list_items = [f"<li>{item[2:].strip()}</li>" for item in list_items]
            block_node = f"<{block_tag}>" + "".join(list_items) + f"</{block_tag}>"
            block_nodes.append(block_node)
        elif block_tag == "code":
            if "\n" not in block:
                code_text = block[3:-3]
            else:
                lines = block.split("\n")
                code_lines = lines[1:-1]
                code_text = "\n".join(line.strip() for line in code_lines) + "\n"
            block_node = f"<pre><code>{code_text}</code></pre>"
            block_nodes.append(block_node)
            # block_node = f"<pre><{block_tag}>" + block[3:-3].strip() + f"</{block_tag}></pre>"
            # block_nodes.append(block_node)
        else:
            block_node = f"<{block_tag}>{block}</{block_tag}>"
            block_nodes.append(block_node)
    return block_nodes


def block_nodes_to_html(block_nodes):
    html_block_nodes = ""
    for block in block_nodes:
        if "<pre><code>" in block:
            html_block_nodes += text_node_to_html_node(TextNode(block, TextTypes.TEXT)).to_html()
        else:
            html_nodes_list = (text_to_textnodes(block))

            for html_node in html_nodes_list:
                html_block_nodes += "" + text_node_to_html_node(html_node).to_html()
    return "<div>" + html_block_nodes + "</div>"



# md = """
# This is **bolded** paragraph
# text in a p
# tag here

# This is another paragraph with _italic_ text and `code` here

# """
# md2 = """
# ```
# This is text that _should_ remain
# the **same** even with inline stuff
# ```
# """

# blocks = blocks_to_BlockNodes(markdown_to_blocks(md))

# print(block_nodes_to_html(blocks))