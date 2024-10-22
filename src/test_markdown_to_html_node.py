import unittest
from helpers import \
    get_ul_li_items_content, \
    get_ol_li_items_content, \
    get_quote_text, \
    text_to_textnodes, \
    text_node_to_html_node, \
    text_to_children, \
    lines_list_to_children, \
    children_to_ul, \
    children_to_ol, \
    markdown_to_html_node
from parentnode import ParentNode   
from htmlnode import HTMLNode
from leafnode import LeafNode

class TestMtHN(unittest.TestCase):
    def test_get_ol_li_lines_1(self):
        text = "1. hola\n2. chau"
        self.assertEqual(["hola", "chau"], get_ol_li_items_content(text))    

    def test_get_ol_li_lines_2(self):
        text = "1. hola\n22. chau"
        self.assertEqual(["hola", "chau"], get_ol_li_items_content(text))

    def test_get_ol_li_lines_3(self):
        text = "10000. hola 22. chau"
        self.assertEqual(["hola 22. chau"], get_ol_li_items_content(text))
      

    def test_get_ul_li_lines_1(self):
        text = "* hola\n* chau"
        self.assertEqual(["hola", "chau"], get_ul_li_items_content(text))

    def test_get_ul_li_lines_2(self):
        text = "* hola\n> chau"
        self.assertEqual(["hola", "chau"], get_ul_li_items_content(text))

    def test_get_ul_li_lines_3(self):
        text = "* hola * chau"
        self.assertEqual(["hola * chau"], get_ul_li_items_content(text))


    def test_get_quote_text_1(self):
        text = "> cita\n> cita\n> cita\n> cita\n"        
        self.assertEqual("cita cita cita cita", get_quote_text(text))

    def test_get_quote_text_2(self):
        text = "> cita cita cita cita"
        self.assertEqual("cita cita cita cita", get_quote_text(text))

    def test_get_quote_text_3(self):
        text = "hola hola"
        self.assertRaises(Exception, get_quote_text(text ))

    def test_get_quote_text_4(self):
        text = "> cita"
        self.assertEqual("cita", get_quote_text(text))


    def test_text_to_children_1(self):
        text = "Hola **bold** *italic* `code` **otro bold**"
        nodes = text_to_textnodes(text)
        leafs = []
        for node in nodes:
            leafs.append(text_node_to_html_node(node))
        self.assertEqual(leafs, text_to_children(text))

    def test_text_to_children_empty(self):
        text = ""
        self.assertEqual(text_to_children(text), [])

    def test_text_to_children_plain_text(self):
        text = "Just a plain text."
        expected = [text_node_to_html_node(node) for node in text_to_textnodes(text)]
        self.assertEqual(text_to_children(text), expected)

    def test_text_to_children_special_characters(self):
        text = "Text with special characters like <, >, &"
        expected = [text_node_to_html_node(node) for node in text_to_textnodes(text)]
        self.assertEqual(text_to_children(text), expected)

    def test_text_to_children_nested_formatting(self):
        text = "**bold *italic* bold**"
        expected = [text_node_to_html_node(node) for node in text_to_textnodes(text)]
        self.assertEqual(text_to_children(text), expected)
    
    
    def test_lines_list_to_children(self):
        lines = ["Work", "About me", "projects"]
        expected = [ParentNode("li", text_to_children(line)) for line in lines]
        self.assertEqual(lines_list_to_children(lines), expected)

    def test_lines_list_to_children_formatting(self):
        lines = ["```Work```", "About *me*", "**projects**"]
        expected = [ParentNode("li", text_to_children(line)) for line in lines]
        self.assertEqual(lines_list_to_children(lines), expected)

    def test_lines_list_to_children_empty(self):
        lines = []
        expected = []
        self.assertEqual(lines_list_to_children(lines), expected)
   
    def test_children_to_ul(self):
        lines = "```Work``` About *me* **projects**"
        children = text_to_children(lines)
        ul = ParentNode("ul", children)
        self.assertEqual(ul, children_to_ul(children))
    
    def test_children_to_ol(self):
        lines = "```Work``` About *me* **projects**"
        children = text_to_children(lines)
        ol = ParentNode("ol", children)
        self.assertEqual(ol, children_to_ol(children))


    def test_markdown_to_html_node_returns_HTMLNode(self):
        node = HTMLNode("div", None,  [])
        markdown = ""
        self.assertEqual(node, markdown_to_html_node(markdown))

    def test_mthn_only_text(self):
        markdown = "this is the markdown contained by the div"
        p = [ParentNode("p", [LeafNode(markdown)])]
        node = HTMLNode("div", None, p)
        expected = markdown_to_html_node(markdown)
        self.assertEqual(node, expected)
        
    def test_mthn_ul(self):
        markdown = "* item 1\n* item 2\n* item 3"
        lines = get_ul_li_items_content(markdown)
        children = lines_list_to_children(lines)
        ul = children_to_ul(children)
        node = HTMLNode("div", None, [ul])
        expected = markdown_to_html_node(markdown)
        self.assertEqual(node, expected)

    def test_mthn_ol(self):
        markdown = "1. item 1\n2. item 2\n3. item 3"
        lines = get_ol_li_items_content(markdown)
        children = lines_list_to_children(lines)
        ol = children_to_ol(children)
        node = HTMLNode("div", None, [ol])
        expected = markdown_to_html_node(markdown)
        self.assertEqual(node, expected)

    def test_mthn_heading(self):
        markdown = "# h1\n\n## h2"
        children = [
            ParentNode("h1", [LeafNode("h1")]),
            ParentNode("h2", [LeafNode("h2")])
        ]
        node = HTMLNode("div", None, children)
        expected = markdown_to_html_node(markdown)
        self.assertEqual(node, expected)

