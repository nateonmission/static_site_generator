import unittest

from main import text_node_to_html_node
from textnode import TextNode, TextTypes
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

class TestMain(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextTypes.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    # def test_text(self):
    #     node = TextNode("hello", TextTypes.TEXT)
    #     expected = LeafNode(None, "hello")
    #     self.assertEqual(text_node_to_html_node(node), expected)

    # def test_bold(self):
    #     node = TextNode("hello", TextTypes.BOLD)
    #     expected = LeafNode("b", "hello")
    #     self.assertEqual(text_node_to_html_node(node), expected)

    # def test_italic(self):
    #     node = TextNode("hello", TextTypes.ITALIC)
    #     expected = LeafNode("i", "hello")
    #     self.assertEqual(text_node_to_html_node(node), expected)

    # def test_code(self):
    #     node = TextNode("print('x')", TextTypes.CODE)
    #     expected = LeafNode("code", "print('x')")
    #     self.assertEqual(text_node_to_html_node(node), expected)

    # def test_link(self):
    #     node = TextNode("Click here", TextTypes.LINK, "https://www.example.com")
    #     expected = LeafNode("a", "Click here", {"href": "https://www.example.com"})
    #     self.assertEqual(text_node_to_html_node(node), expected)

    # def test_image(self):
    #     node = TextNode("alt text", TextTypes.IMAGE, "https://www.example.com/image.png")
    #     expected = LeafNode("img", "", {"src": "https://www.example.com/image.png", "alt": "alt text"})
    #     self.assertEqual(text_node_to_html_node(node), expected)

    # def test_invalid_text_type(self):
    #     node = TextNode("oops", "unknown")
    #     with self.assertRaises(ValueError):
    #         text_node_to_html_node(node)