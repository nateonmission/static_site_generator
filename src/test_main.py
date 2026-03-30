import unittest

from main import extract_title


class TestTextNode(unittest.TestCase):
    def test_extract_title(self):
        markdown = """# This is the title"""
        self.assertEqual(extract_title(markdown), "This is the title")  
        
    def test_extract_title_with_content(self):
        markdown = """# This is the title
This is some content. ## This is a subtitle."""
        self.assertEqual(extract_title(markdown), "This is the title")  
        
    def test_extract_title_no_title(self):
        markdown = """This is some content. ## This is a subtitle."""
        with self.assertRaises(ValueError):
            extract_title(markdown)
            
    def test_extract_title_no_title_only_subtitle(self):
        markdown = """## This is a subtitle."""
        with self.assertRaises(ValueError):
            extract_title(markdown)