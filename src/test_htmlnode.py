import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()
            
    def test_props_to_html(self):
        node = HTMLNode(props={"class": "my-class", "id": "my-id"})
        self.assertEqual(node.props_to_html(), ' class="my-class" id="my-id"')
        
    def test_repr(self):
        node = HTMLNode(tag="div", children=["child1", "child2"], value="Hello", props={"class": "my-class"})
        self.assertEqual(repr(node), "HTMLNode(tag=div, children=['child1', 'child2'], value=Hello, props={'class': 'my-class'})")
        