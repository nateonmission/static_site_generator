import unittest

from blocknode import block_to_block_type, BlockTypes


class TestBlockNode(unittest.TestCase):
    def test_block_types_basic(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockTypes.HEADING)
        self.assertEqual(block_to_block_type("```code```"), BlockTypes.CODE)
        self.assertEqual(block_to_block_type("> quote"), BlockTypes.QUOTE)
        self.assertEqual(block_to_block_type("- item"), BlockTypes.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. item"), BlockTypes.ORDERED_LIST)
        self.assertEqual(block_to_block_type("just text"), BlockTypes.PARAGRAPH)
        
    def test_ordered_list_multi_digit(self):
        self.assertEqual(block_to_block_type("10. item"), BlockTypes.ORDERED_LIST)
        
    def test_missing_space_after_marker(self):
        self.assertEqual(block_to_block_type("#Heading"), BlockTypes.PARAGRAPH)
        self.assertEqual(block_to_block_type(">quote"), BlockTypes.PARAGRAPH)
        self.assertEqual(block_to_block_type("-item"), BlockTypes.PARAGRAPH)
        self.assertEqual(block_to_block_type("1.item"), BlockTypes.PARAGRAPH)
        
    def test_leading_whitespace(self):
        self.assertEqual(block_to_block_type("   # Heading"), BlockTypes.PARAGRAPH)
        
    def test_code_block_open_only(self):
        self.assertEqual(block_to_block_type("```"), BlockTypes.CODE)
        
    def test_false_positive_patterns(self):
        self.assertEqual(block_to_block_type("123 text"), BlockTypes.PARAGRAPH)
        self.assertEqual(block_to_block_type("-not a list"), BlockTypes.PARAGRAPH)
        self.assertEqual(block_to_block_type(">not quote"), BlockTypes.PARAGRAPH)