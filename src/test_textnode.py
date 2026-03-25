import unittest

from textnode import TextNode, TextTypes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextTypes.BOLD, "https://www.example.com")
        node2 = TextNode("This is a text node", TextTypes.BOLD, "https://www.example.com")
        self.assertEqual(node, node2)
        
    def test_repr(self):
        node = TextNode("This is a text node", TextTypes.BOLD, "https://www.example.com")
        self.assertEqual(repr(node), "TextNode(This is a text node, TextTypes.BOLD, https://www.example.com)")
        
    def test_inequality(self):
        node = TextNode("This is a text node", TextTypes.BOLD, "https://www.example.com")
        node2 = TextNode("This is a different text node", TextTypes.ITALIC, "https://www.example.com")
        self.assertNotEqual(node, node2)
        
    def test_url(self):
        node = TextNode("This is a text node", TextTypes.LINK, "https://www.example.com")
        self.assertEqual(node.url, "https://www.example.com")


if __name__ == "__main__":
    unittest.main()