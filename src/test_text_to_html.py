import unittest

from helpers import text_node_to_html_node, extract_markdown_links, extract_markdown_images, split_nodes_delimiter
from textnode import TextNode
from leafnode import LeafNode

class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("texto", "text")
        html = text_node_to_html_node(node)

        self.assertIsInstance(html, LeafNode)
        self.assertEqual(html, LeafNode("texto"))
    
    def test_bold(self):
        node = TextNode("texto", "bold")
        html = text_node_to_html_node(node)
        self.assertIsInstance(html, LeafNode)

        self.assertEqual(html, LeafNode("texto", "b"))
    
    def test_italic(self):
        node = TextNode("texto", "italic")
        html = text_node_to_html_node(node)
        self.assertIsInstance(html, LeafNode)

        self.assertEqual(html, LeafNode("texto", "i"))
    
    def test_code(self):
        node = TextNode("texto", "code")
        html = text_node_to_html_node(node)
        self.assertIsInstance(html, LeafNode)

        self.assertEqual(html, LeafNode("texto", "code"))
    
    def test_link(self):
        node = TextNode("texto", "link", "link.com")
        html = text_node_to_html_node(node)
        self.assertIsInstance(html, LeafNode)

        self.assertEqual(html, LeafNode("texto", "a", {"href": "link.com"}))
    
    def test_image(self):
        node = TextNode("texto", "image", "image.com")
        html = text_node_to_html_node(node)
        self.assertIsInstance(html, LeafNode)

        self.assertEqual(html, LeafNode("", "img", {"src": "image.com", "alt":"texto"}))
    
    def test_exception(self):
        node = TextNode("texto", "img")
        self.assertRaises(Exception, text_node_to_html_node, node)


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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_a(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_results = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        results = extract_markdown_images(text)
        self.assertEqual(results, expected_results)

    def test_mixed_with_links(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) click here to see it [link](https://link.com.ar)"
        expected_results = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        results = extract_markdown_images(text)
        self.assertEqual(results, expected_results)
    
    def test_only_links(self):
        text = "click here to see it [link](https://link.com.ar) or here to [buy](https://buy.com)"
        expected_results = []
        results = extract_markdown_images(text)
        self.assertEqual(results, expected_results)

class TestExtractMarkdownLink(unittest.TestCase):
    def test_base(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_results = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        results = extract_markdown_links(text)
        self.assertEqual(results, expected_results)
    def test_only_link(self):
        text = "[to boot dev](https://www.boot.dev)"
        expected_results = [("to boot dev", "https://www.boot.dev")]
        results = extract_markdown_links(text)
        self.assertEqual(results, expected_results)
    
    def test_mixed_with_images(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_results = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        results = extract_markdown_links(text)
        self.assertEqual(results, expected_results)
    
    def only_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_results = []
        results = extract_markdown_links(text)
        self.assertEqual(results, expected_results)


