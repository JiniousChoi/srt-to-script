#!/usr/bin/python3

from .context import src

import unittest


class TagParserTest(unittest.TestCase):
    
    def test_parse_tag(self):
        text_with_tags = 'Hello <font color="#80ff80">Potter</font>!!<a href="#">Visit me</a> Later'
        actual = src.strip_tags(text_with_tags)
        expected = 'Hello Potter!!Visit me Later'
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
