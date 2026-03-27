import unittest
from textnode import TextNode, TextTypes
from textprocessing import split_nodes_delimiter, extract_markdown_images, split_nodes_image, split_nodes_link


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextTypes.TEXT)
        result = split_nodes_delimiter([node], "`", TextTypes.CODE)
        expected = [
            TextNode("This is text with a ", TextTypes.TEXT),
            TextNode("code block", TextTypes.CODE),
            TextNode(" word", TextTypes.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_bold_delimiter(self):
        node = TextNode("This is **bold** text", TextTypes.TEXT)
        result = split_nodes_delimiter([node], "**", TextTypes.BOLD)
        expected = [
            TextNode("This is ", TextTypes.TEXT),
            TextNode("bold", TextTypes.BOLD),
            TextNode(" text", TextTypes.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_italic_delimiter(self):
        node = TextNode("This is *italic* text", TextTypes.TEXT)
        result = split_nodes_delimiter([node], "*", TextTypes.ITALIC)
        expected = [
            TextNode("This is ", TextTypes.TEXT),
            TextNode("italic", TextTypes.ITALIC),
            TextNode(" text", TextTypes.TEXT),
        ]
        self.assertEqual(result, expected)
        
    def test_multiple_code_sections(self):
        node = TextNode("Use `a` and `b` here", TextTypes.TEXT)
        result = split_nodes_delimiter([node], "`", TextTypes.CODE)
        expected = [
            TextNode("Use ", TextTypes.TEXT),
            TextNode("a", TextTypes.CODE),
            TextNode(" and ", TextTypes.TEXT),
            TextNode("b", TextTypes.CODE),
            TextNode(" here", TextTypes.TEXT),
        ]
        self.assertEqual(result, expected)
        
    def test_non_text_nodes_unchanged(self):
        old_nodes = [
            TextNode("already bold", TextTypes.BOLD),
            TextNode("plain `code` text", TextTypes.TEXT),
        ]
        result = split_nodes_delimiter(old_nodes, "`", TextTypes.CODE)
        expected = [
            TextNode("already bold", TextTypes.BOLD),
            TextNode("plain ", TextTypes.TEXT),
            TextNode("code", TextTypes.CODE),
            TextNode(" text", TextTypes.TEXT),
        ]
        self.assertEqual(result, expected)
        
    def test_raises_on_missing_closing_delimiter(self):
        node = TextNode("This is `broken text", TextTypes.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextTypes.CODE)
            
    def test_raises_on_unknown_delimiter(self):
        node = TextNode("This is ~weird~ text", TextTypes.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "~", TextTypes.ITALIC)
            
    def test_no_delimiter_present(self):
        node = TextNode("Just plain text", TextTypes.TEXT)
        result = split_nodes_delimiter([node], "`", TextTypes.CODE)
        expected = [TextNode("Just plain text", TextTypes.TEXT)]
        self.assertEqual(result, expected)

    def test_delimiter_at_start_and_end(self):
        node = TextNode("`code`", TextTypes.TEXT)
        result = split_nodes_delimiter([node], "`", TextTypes.CODE)
        expected = [TextNode("code", TextTypes.CODE)]
        self.assertEqual(result, expected)

    def test_empty_input_list(self):
        result = split_nodes_delimiter([], "`", TextTypes.CODE)
        self.assertEqual(result, [])
        
    def test_multiple_nodes(self):
        old_nodes = [
            TextNode("This is `code`", TextTypes.TEXT),
            TextNode(" and this is plain", TextTypes.TEXT),
        ]
        result = split_nodes_delimiter(old_nodes, "`", TextTypes.CODE)
        expected = [
            TextNode("This is ", TextTypes.TEXT),
            TextNode("code", TextTypes.CODE),
            TextNode(" and this is plain", TextTypes.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_empty_bold_section(self):
        node = TextNode("This is **** text", TextTypes.TEXT)
        result = split_nodes_delimiter([node], "**", TextTypes.BOLD)
        expected = [
            TextNode("This is ", TextTypes.TEXT),
            TextNode(" text", TextTypes.TEXT),
        ]
        self.assertEqual(result, expected)
        
    # IMAGE CAPTURING TEST
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_multiple_images(self):
        matches = extract_markdown_images("Here is ![rick](url1) and ![obi](url2)")
        expected = [
            ("rick", "url1"),
            ("obi", "url2"),
        ]
        self.assertEqual(matches, expected)
            
    def test_no_images(self):
        text = "This is just plain text"
        matches =  extract_markdown_images(text)
        self.assertEqual(matches, [])
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextTypes.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextTypes.TEXT),
                TextNode("image", TextTypes.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextTypes.TEXT),
                TextNode(
                    "second image", TextTypes.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_images_no_images(self):
        node = TextNode("This is just plain text", TextTypes.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is just plain text", TextTypes.TEXT)],
            new_nodes,
        )

    def test_split_images_at_edges(self):
        node = TextNode(
            "![start](https://example.com/start.png) middle ![end](https://example.com/end.png)",
            TextTypes.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextTypes.IMAGE, "https://example.com/start.png"),
                TextNode(" middle ", TextTypes.TEXT),
                TextNode("end", TextTypes.IMAGE, "https://example.com/end.png"),
            ],
            new_nodes,
        )


    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextTypes.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextTypes.TEXT),
                TextNode("link", TextTypes.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextTypes.TEXT),
                TextNode(
                    "second link", TextTypes.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_links_no_links(self):
        node = TextNode("This is just plain text", TextTypes.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is just plain text", TextTypes.TEXT)],
            new_nodes,
        )
        
    def test_split_links_at_edges(self):
        node = TextNode(
            "[start](https://example.com) middle [end](https://example.org)",
            TextTypes.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("start", TextTypes.LINK, "https://example.com"),
                TextNode(" middle ", TextTypes.TEXT),
                TextNode("end", TextTypes.LINK, "https://example.org"),
            ],
            new_nodes,
        )