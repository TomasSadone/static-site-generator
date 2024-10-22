import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_no_value(self):
        node = LeafNode(None, "p", {"class": "paragraph"})
        self.assertRaises(ValueError, node.to_html)


    def test_no_tag(self):
        value = "value"
        node = LeafNode(value, None, {"class": "paragraph"})
        s = node.to_html()
        self.assertEqual(s, value)


    def test_tag(self):
        node = LeafNode("value", "p", {"class": "paragraph"})
        tag = "<p class=\"paragraph\">value</p>"
        self.assertEqual(node.to_html(), tag)