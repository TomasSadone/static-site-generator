import unittest

from textnode import TextNode
from helpers import split_nodes_link

class TestSplitNodesLink(unittest.TestCase):
    def test_no_link(self):
        nodes = [
            TextNode("Este es un texto","text"),
            TextNode("Este es `otro` texto","text"),
            TextNode("Este es el ultimo de los textos","text")
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(result, nodes)


    def test_one_link(self):
        nodes = [
            TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) link", "text")
        ]
        expected_result = [
            TextNode("This is text with a ", "text"),
            TextNode("rick roll", "link", "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" link", "text"),
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(result, expected_result)
    
    def test_one_link_no_empty_nodes(self):
        nodes = [
            TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif)", "text")
        ]
        expected_result = [
            TextNode("This is text with a ", "text"),
            TextNode("rick roll", "link", "https://i.imgur.com/aKaOqIh.gif")
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(result, expected_result)
    
    
    def test_multiple_links_in_one_node(self):
        nodes = [
            TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", "text")
        ]
        expected_result = [
            TextNode("This is text with a ", "text"),
            TextNode("rick roll", "link", "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", "text"),
            TextNode("obi wan", "link", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(result, expected_result)

    def test_multiple_nodes_one_link(self):
        nodes = [
            TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif)", "text"),
            TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif)", "text"),
            TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif)", "text")
        ]
        expected_result = [
            TextNode("This is text with a ", "text"),
            TextNode("rick roll", "link", "https://i.imgur.com/aKaOqIh.gif"),
            TextNode("This is text with a ", "text"),
            TextNode("rick roll", "link", "https://i.imgur.com/aKaOqIh.gif"),
            TextNode("This is text with a ", "text"),
            TextNode("rick roll", "link", "https://i.imgur.com/aKaOqIh.gif"),
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(result, expected_result)

    def test_multiple_links_in_multiple_nodes(self):
        nodes = [
            TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", "text"),
            TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", "text"),
            TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", "text"),
        ]
        expected_result = [
            TextNode("This is text with a ", "text"),
            TextNode("rick roll", "link", "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", "text"),
            TextNode("obi wan", "link", "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode("This is text with a ", "text"),
            TextNode("rick roll", "link", "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", "text"),
            TextNode("obi wan", "link", "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode("This is text with a ", "text"),
            TextNode("rick roll", "link", "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", "text"),
            TextNode("obi wan", "link", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(result, expected_result)


