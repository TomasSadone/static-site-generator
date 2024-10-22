import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_2(self):
        node = TextNode("Nodo", "italic", None)
        node2 = TextNode("Nodo", "italic", None)
        self.assertEqual(node, node2)

    def test_eq_3(self):
        node = TextNode("Nodo", "italic", "asdfasdf")
        node2 = TextNode("Nodo", "italic", 'asdfasdf')
        self.assertEqual(node, node2)

    def test_eq_4(self):
        node = TextNode("Nodo", "italic", None)
        node2 = TextNode("Nodo2", "italic", None)
        self.assertNotEqual(node, node2)

    def test_eq_5(self):
        node = TextNode("Nodo", "bold", None)
        node2 = TextNode("Nodo", "italic", None)
        self.assertNotEqual(node, node2)

    def test_eq_6(self):
        node = TextNode("Nodo", "bold")
        node2 = TextNode("Nodo", "bold", None)
        self.assertEqual(node, node2)

    def test_eq_7(self):
        node = TextNode("Nodo", "bold", "url")
        node2 = TextNode("Nodo", "italic", None)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()