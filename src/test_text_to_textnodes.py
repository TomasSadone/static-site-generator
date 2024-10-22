import unittest

from textnode import TextNode
from helpers import text_to_textnodes

class TestTextToTextnodes(unittest.TestCase):
    def integration_a(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_result =   [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("obi wan image", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ]   
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_result)
    
    def test_only_bold(self):
        text = "**bold**"
        expected = [TextNode("bold", "bold")]
        result = text_to_textnodes(text)
        self.assertEqual(expected, result)


