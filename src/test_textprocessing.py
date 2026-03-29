import unittest
from textnode import TextNode, TextTypes
from textprocessing import split_nodes_delimiter, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, blocks_to_BlockNodes, block_nodes_to_html


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
        node = TextNode("This is _italic_ text", TextTypes.TEXT)
        result = split_nodes_delimiter([node], "_", TextTypes.ITALIC)
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
        
    def test_text_to_textnodes_all_types(self):
        text = "This is **bold** and _italic_ and `code` and ![img](imgurl) and [link](linkurl)"
        
        result = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextTypes.TEXT),
            TextNode("bold", TextTypes.BOLD),
            TextNode(" and ", TextTypes.TEXT),
            TextNode("italic", TextTypes.ITALIC),
            TextNode(" and ", TextTypes.TEXT),
            TextNode("code", TextTypes.CODE),
            TextNode(" and ", TextTypes.TEXT),
            TextNode("img", TextTypes.IMAGE, "imgurl"),
            TextNode(" and ", TextTypes.TEXT),
            TextNode("link", TextTypes.LINK, "linkurl"),
        ]

        self.assertEqual(result, expected)
        
    
    def test_text_to_textnodes_plain(self):
        text = "Just plain text"
        result = text_to_textnodes(text)

        expected = [
            TextNode("Just plain text", TextTypes.TEXT)
        ]

        self.assertEqual(result, expected)
        
        
    def test_text_to_textnodes_multiple_bold(self):
        text = "**one** and **two**"
        result = text_to_textnodes(text)

        expected = [
            TextNode("one", TextTypes.BOLD),
            TextNode(" and ", TextTypes.TEXT),
            TextNode("two", TextTypes.BOLD),
        ]

        self.assertEqual(result, expected)
        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_to_blocks_irregular_spacing(self):
        markdown = "First block\n\n\n   \nSecond block\n\n   Third block   "
        result = markdown_to_blocks(markdown)

        expected = [
            "First block",
            "Second block",
            "Third block",
        ]

        self.assertEqual(result, expected)
        
    def test_markdown_to_blocks_leading_trailing_newlines(self):
        markdown = "\n\nFirst\n\nSecond\n\n"
        result = markdown_to_blocks(markdown)

        expected = [
            "First",
            "Second",
        ]

        self.assertEqual(result, expected)
        
    def test_markdown_to_blocks_preserves_internal_newlines(self):
        markdown = "Line 1\nLine 2\n\nParagraph 2\nLine B"
        result = markdown_to_blocks(markdown)

        expected = [
            "Line 1\nLine 2",
            "Paragraph 2\nLine B",
        ]

        self.assertEqual(result, expected)
    
    
    # BLOCKS TO BLOCKNODES TESTS    
    def test_heading_level_3(self):
        blocks = ["### Hello"]
        result = blocks_to_BlockNodes(blocks)
        self.assertEqual(result, ["<h3>Hello</h3>"])

    def test_paragraph_block(self):
        blocks = ["This is a paragraph."]
        result = blocks_to_BlockNodes(blocks)
        self.assertEqual(result, ["<p>This is a paragraph.</p>"])

    def test_code_block(self):
        blocks = ["```print('hi')```"]
        result = blocks_to_BlockNodes(blocks)
        self.assertEqual(result, ["<pre><code>print('hi')</code></pre>"])

    def test_quote_block(self):
        blocks = ["> quoted text"]
        result = blocks_to_BlockNodes(blocks)
        self.assertEqual(result, ["<blockquote>> quoted text</blockquote>"])

    def test_unordered_list_multiple_items(self):
        blocks = ["- one\n- two\n- three"]
        result = blocks_to_BlockNodes(blocks)
        self.assertEqual(
            result,
            ["<ul><li>one</li><li>two</li><li>three</li></ul>"]
        )

    def test_ordered_list_multiple_items(self):
        blocks = ["1. first\n2. second\n3. third"]
        result = blocks_to_BlockNodes(blocks)
        self.assertEqual(
            result,
            ["<ol><li>first</li><li>second</li><li>third</li></ol>"]
        )

    def test_mixed_blocks(self):
        blocks = [
            "# Title",
            "This is text.",
            "- one\n- two",
            "> quote",
        ]
        result = blocks_to_BlockNodes(blocks)
        self.assertEqual(
            result,
            [
                "<h1>Title</h1>",
                "<p>This is text.</p>",
                "<ul><li>one</li><li>two</li></ul>",
                "<blockquote>> quote</blockquote>",
            ]
        )
        
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = blocks_to_BlockNodes(markdown_to_blocks(md))
        html = block_nodes_to_html(node)
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
            md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

            node = blocks_to_BlockNodes(markdown_to_blocks(md))
            html = block_nodes_to_html(node)
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )
            
    def test_empty_codeblock(self):
        md = """
        ```
        ```
        """
        node = blocks_to_BlockNodes(markdown_to_blocks(md))
        html = block_nodes_to_html(node)
        self.assertEqual(
            html,
            "<div><pre><code>\n</code></pre></div>",
        )
        
    def test_codeblock_single_line_with_symbols(self):
        md = "```x = 1 < 2 and y == '**not bold**'```"
        node = blocks_to_BlockNodes(markdown_to_blocks(md))
        html = block_nodes_to_html(node)
        self.assertEqual(
            html,
            "<div><pre><code>x = 1 < 2 and y == '**not bold**'</code></pre></div>",
        )
        
    def test_codeblock_with_literal_image_and_link_syntax(self):
        md = """
        ```
        ![alt](img.png)
        [link](https://boot.dev)
        ```
        """
        node = blocks_to_BlockNodes(markdown_to_blocks(md))
        html = block_nodes_to_html(node)
        self.assertEqual(
            html,
            "<div><pre><code>![alt](img.png)\n[link](https://boot.dev)\n</code></pre></div>",
        )
        
        
    def test_live_readme_from_GitHub(self):
        self.maxDiff = None
        md="""![Alt Text](https://res.cloudinary.com/wesbos/image/upload/v1574876851/BJS/BJS-Social-Share.png)

# Beginner JavaScript

These are the starter files and solutions to the [Beginner JavaScript](https://BeginnerJavaScript.com) course

## Function Definition Diagram

![Description of javaScript function](function-definition.jpg)

## Community Resources

Please feel free to add your blog post, videos, notes, or anything else related to the course :)

- [Soumya Ranjan Mohanty](https://github.com/geekysrm) [Github repo](https://github.com/geekysrm/javascript-notes) with notes and lessons learnt, along with [full notes here](https://notes.soumya.dev/javascript).
- [Linda has documented all her excercises on Codepen](https://twitter.com/lindakatcodes/status/1331702581220020225)
- [Cesar Gomez](https://github.com/CsarGomez) have a [GitHub repo](https://github.com/CsarGomez/beginnersJavascriptNotes) with notes for all the modules completed including exercises in [CopePen](https://codepen.io/collection/XjJQYz) other modules will be uploaded a soon as i finished each one
"""
        blocks = blocks_to_BlockNodes(markdown_to_blocks(md))
        html = block_nodes_to_html(blocks)

        expected = (
        "<div>"
        '<p><img src="https://res.cloudinary.com/wesbos/image/upload/v1574876851/BJS/BJS-Social-Share.png" alt="Alt Text" /></p>'
        "<h1>Beginner JavaScript</h1>"
        '<p>These are the starter files and solutions to the <a href="https://BeginnerJavaScript.com">Beginner JavaScript</a> course</p>'
        "<h2>Function Definition Diagram</h2>"
        '<p><img src="function-definition.jpg" alt="Description of javaScript function" /></p>'
        "<h2>Community Resources</h2>"
        "<p>Please feel free to add your blog post, videos, notes, or anything else related to the course :)</p>"
        "<ul>"
        '<li><a href="https://github.com/geekysrm">Soumya Ranjan Mohanty</a> <a href="https://github.com/geekysrm/javascript-notes">Github repo</a> with notes and lessons learnt, along with <a href="https://notes.soumya.dev/javascript">full notes here</a>.</li>'
        '<li><a href="https://twitter.com/lindakatcodes/status/1331702581220020225">Linda has documented all her excercises on Codepen</a></li>'
        '<li><a href="https://github.com/CsarGomez">Cesar Gomez</a> have a <a href="https://github.com/CsarGomez/beginnersJavascriptNotes">GitHub repo</a> with notes for all the modules completed including exercises in <a href="https://codepen.io/collection/XjJQYz">CopePen</a> other modules will be uploaded a soon as i finished each one</li>'
        "</ul>"
        "</div>"
        )

        self.assertEqual(html, expected)

