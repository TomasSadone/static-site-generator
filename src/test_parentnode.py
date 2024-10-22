import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_one_level_deep(self):
        node = ParentNode(
            "p",
            [
                LeafNode("Bold text", "b"),
                LeafNode("Normal text"),
                LeafNode("italic text", "i"),
                LeafNode("Normal text"),
            ],
        )
        html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(html, node.to_html())

    def test_parentnode_tag_error(self):
        node = ParentNode(None,[
                    LeafNode("Bold text", "b"),
                    LeafNode("Normal text"),
                    LeafNode("italic text", "i"),
                    LeafNode("Normal text"),
                ])
        
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "ParentNode must have a tag")


    def test_parentnode_children_error(self):
        node = ParentNode("div", None)
        
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "ParentNode must have children")

    def test_multiple_levels_deep(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "div",
                    [
                        LeafNode("hola que tal", "p"),
                        ParentNode("div", [LeafNode("como va", "p")])
                    ]
                ),
                LeafNode("Normal text"),
                LeafNode("italic text", "i"),
                LeafNode("Normal text"),
            ],
        )
        html = "<div><div><p>hola que tal</p><div><p>como va</p></div></div>Normal text<i>italic text</i>Normal text</div>"
        self.assertEqual(node.to_html(), html)


    def test_multiple_levels_deep_tag_error(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "div",
                    [
                        LeafNode("hola que tal", "p"),
                        ParentNode(None, [LeafNode("como va", "p")])
                    ]
                ),
                LeafNode("Normal text"),
                LeafNode("italic text", "i"),
                LeafNode("Normal text"),
            ],
        )
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "ParentNode must have a tag")
    
    
    def test_multiple_levels_deep_children_error(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "div",
                    [
                        LeafNode("hola que tal", "p"),
                        ParentNode("p", None)
                    ]
                ),
                LeafNode("Normal text"),
                LeafNode("italic text", "i"),
                LeafNode("Normal text"),
            ],
        )
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), "ParentNode must have children")
