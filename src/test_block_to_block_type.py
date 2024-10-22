import unittest

from helpers import block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        text = "# Heading"
        self.assertEqual(block_to_block_type(text), "heading")

    def test_heading_2(self):
        text = "## Heading"
        self.assertEqual(block_to_block_type(text), "heading")

    def test_heading_3(self):
        text = "### Heading"
        self.assertEqual(block_to_block_type(text), "heading")

    def test_heading_4(self):
        text = "#### Heading"
        self.assertEqual(block_to_block_type(text), "heading")

    def test_heading_5(self):
        text = "##### Heading"
        self.assertEqual(block_to_block_type(text), "heading")

    def test_heading_6(self):
        text = "###### Heading"
        self.assertEqual(block_to_block_type(text), "heading")

    def test_heading_7(self):
        text = "######## Heading"
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_code_block(self):
        text = "```function codigo(){return null}```"
        self.assertEqual(block_to_block_type(text), "code")
    
    def test_wrong_code_block(self):
        text = "````function codigo(){return null}```"
        self.assertEqual(block_to_block_type(text), "paragraph")
    
    def test_wrong_code_block_2(self):
        text = "```function codigo(){return null}````"
        self.assertEqual(block_to_block_type(text), "paragraph")
    
    def test_quote(self):
        text = "> galaaaaaaaatii"
        self.assertEqual(block_to_block_type(text), "quote")
    
    def test_wrong_quote(self):
        text = ">> galaaaaaaaatii"
        self.assertEqual(block_to_block_type(text), "paragraph")
    
    def test_unordered_list(self):
        text = "* galaaaaaaaatii\n- otro\n* te la cambio de nuevo"
        self.assertEqual(block_to_block_type(text), "unordered_list")
    
    def test_unordered_list(self):
        text = "- galaaaaaaaatii"
        self.assertEqual(block_to_block_type(text), "unordered_list")
    
    def test_wrong_unordered_list(self):
        text = "** galaaaaaaaatii"
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_ordered_list(self):
        text = "1. galaaaaati"
        self.assertEqual(block_to_block_type(text), "ordered_list")
    
    def test_wrong_ordered_list(self):
        text = "1.galaaaaati"
        self.assertEqual(block_to_block_type(text), "paragraph")
    
    def test_wrong_ordered_list_2(self):
        text = "a. galaaaaati"
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_paragraph(self):
        text = "!!!dsad dsadsa dsadsa"
        self.assertEqual(block_to_block_type(text), "paragraph")


