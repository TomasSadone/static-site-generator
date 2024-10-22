import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_not_implemented(self):
        node = HTMLNode("div", "hola", None, {"class": "main-content"})
        self.assertRaises(NotImplementedError, node.to_html)

    def test_to_html(self):
        node = HTMLNode("div", "hola", None, {"class": "main-content"})
        s = node.props_to_html()
        s_2 = " class=\"main-content\""
        self.assertEqual(s, s_2)

    def test_to_html_2(self):
        node = HTMLNode("form", "hola", None, {"class": "main-content", "id": "main", "method": "POST"})
        s = node.props_to_html()
        s_2 = " class=\"main-content\" id=\"main\" method=\"POST\""
        self.assertEqual(s, s_2)

    def test_to_html_3(self):
        node = HTMLNode("form", "hola", None)
        s = node.props_to_html()
        self.assertEqual(s, "")


        
