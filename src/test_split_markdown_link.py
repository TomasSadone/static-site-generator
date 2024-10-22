import unittest

from helpers import extract_markdown_links

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


