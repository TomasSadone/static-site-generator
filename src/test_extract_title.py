import unittest
from helpers import extract_title


class TestExtractTitle(unittest.TestCase):
    def TestNormal(self):
        markdown = "# Title\notro contenido\n1. li\n2. li"
        result = extract_title(markdown)
        self.assertEqual(result, "Title")
    
    def TestRaise(self):
        markdown = "#Title\notro contenido\n1. li\n2. li"
        self.assertRaises(Exception, extract_title(markdown))

