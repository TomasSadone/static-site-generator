import unittest

from helpers import extract_markdown_images

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


