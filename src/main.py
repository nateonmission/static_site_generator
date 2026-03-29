
from textnode import TextNode, TextTypes
from leafnode import LeafNode
from htmlnode import HTMLNode
from parentnode import ParentNode
from textprocessing import split_nodes_delimiter, split_nodes_image, split_nodes_link




def main():
    node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    print(node)


if __name__ == "__main__":
    main()
