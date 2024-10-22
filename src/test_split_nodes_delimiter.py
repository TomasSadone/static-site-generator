import unittest

from textnode import TextNode
from helpers import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_plain_text_vs_bold(self):
        old_nodes = [
            TextNode("Este es un texto","text"),
            TextNode("Este es otro texto","text"),
            TextNode("Este es el ultimo de los textos","text")
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", "bold")
        self.assertEqual(old_nodes, new_nodes)
    
    
    def test_plain_and_bold_vs_bold(self):
        old_nodes = [
            TextNode("Este es un texto","text"),
            TextNode("Este es **otro** texto","text"),
            TextNode("Este es el ultimo de los textos","text")
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", "bold")
        new_nodes_expected = [
            TextNode("Este es un texto","text"),
            TextNode("Este es ","text"),
            TextNode("otro","bold"),
            TextNode(" texto","text"),            
            TextNode("Este es el ultimo de los textos","text")
        ]
        self.assertEqual(new_nodes, new_nodes_expected)
    
    
    def test_plain_and_italic_vs_italic(self):
        old_nodes = [
            TextNode("Este es un texto","text"),
            TextNode("Este es *otro* texto","text"),
            TextNode("Este es el ultimo de los textos","text")
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "*", "italic")
        new_nodes_expected = [
            TextNode("Este es un texto","text"),
            TextNode("Este es ","text"),
            TextNode("otro","italic"),
            TextNode(" texto","text"),            
            TextNode("Este es el ultimo de los textos","text")
        ]
        self.assertEqual(new_nodes, new_nodes_expected)


    def test_plain_and_code_vs_code(self):
        old_nodes = [
            TextNode("Este es un texto","text"),
            TextNode("Este es `otro` texto","text"),
            TextNode("Este es el ultimo de los textos","text")
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "`", "code")
        new_nodes_expected = [
            TextNode("Este es un texto","text"),
            TextNode("Este es ","text"),
            TextNode("otro","code"),
            TextNode(" texto","text"),            
            TextNode("Este es el ultimo de los textos","text")
        ]
        self.assertEqual(new_nodes, new_nodes_expected)
    
    def test_start_with_delimiter(self):
        nodes = [TextNode("**texto en negrita** texto comun", "text")]
        new_nodes = split_nodes_delimiter(nodes, "**", "bold")
        self.assertEqual(new_nodes, [TextNode("texto en negrita", "bold"), TextNode(" texto comun", "text")])
    
    
    def test_end_with_delimiter(self):
        nodes = [TextNode("texto comun **texto en negrita**", "text")]
        new_nodes = split_nodes_delimiter(nodes, "**", "bold")
        self.assertEqual(new_nodes, [TextNode("texto comun ", "text"), TextNode("texto en negrita", "bold")])
    
    def test_delimiters_side_to_side(self):
        nodes = [TextNode("**bold***italic*", "text")]
        new_nodes = split_nodes_delimiter(nodes, "**", "bold")
        new_nodes = split_nodes_delimiter(new_nodes, "*", "italic")
        expected_nodes = [TextNode("bold", "bold"), TextNode("italic", "italic")]
        self.assertEqual(new_nodes, expected_nodes)

    def test_only_between_delimiters(self):
        nodes = [TextNode("**bold**", "text")]
        new_nodes = split_nodes_delimiter(nodes, "**", "bold")
        expected_nodes = [TextNode("bold", "bold")]
        self.assertEqual(new_nodes, expected_nodes)

    def test_all_vs_all(self):
        types = [("code", "`"), ("bold", "**"), ("italic", "*")]
        

        old_nodes = [
            TextNode("Este es un texto","text"),
            TextNode("Aca tenemos `otro` texto","text"),
            TextNode("**Y este es** *el ultimo* de los textos","text")
        ]
        for type in types:
            old_nodes = split_nodes_delimiter(old_nodes, type[1], type[0])
        # new_nodes = split_nodes_delimiter(old_nodes, "`", "code")
        new_nodes_expected = [
            TextNode("Este es un texto","text"),
            TextNode("Aca tenemos ","text"),
            TextNode("otro","code"),
            TextNode(" texto","text"),            
            TextNode("Y este es", "bold"),
            TextNode(" ", "text"),
            TextNode("el ultimo", "italic"),
            TextNode(" de los textos", "text")
        ]
        self.assertEqual(old_nodes, new_nodes_expected)



