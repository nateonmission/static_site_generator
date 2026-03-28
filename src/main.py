
from textnode import TextNode, TextTypes
from leafnode import LeafNode
from htmlnode import HTMLNode
from parentnode import ParentNode
from textprocessing import split_nodes_delimiter, split_nodes_image, split_nodes_link




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


def main():
    node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    print(node)


if __name__ == "__main__":
    main()
