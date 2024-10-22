import unittest

from helpers import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_title_paragraph(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it."""
        expected_result = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it."]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected_result)

    def test_trailing_newline(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.
"""
        expected_result = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n"]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected_result)

    def test_more_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        expected_result = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected_result)
    
    def test_extra_new_lines(self):
        markdown = """# This is a heading





This is a paragraph of text. It has some **bold** and *italic* words inside of it.





* This is the first list item in a list block
* This is a list item
* This is another list item


"""
        expected_result = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected_result)


