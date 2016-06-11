#!/usr/bin/python3

from .context import src

import unittest


class TestBasic(unittest.TestCase):
    '''Basic test cases'''

    def test_strip_number_counters(self):
        raw_script = load_file('./tests/sample/subtitle_short.srt')

        actual = src.strip_number_counters(raw_script)

        expected = load_file('./tests/sample/subtitle_short.out0')

        self.assertEqual(actual, expected)


    def test_strip_time_indicator(self):
        raw_script = load_file('./tests/sample/subtitle_short.out0')

        actual = src.strip_time_indicator(raw_script)
        actual = src.strip_empty_lines(actual)

        expected = load_file('./tests/sample/subtitle_short.out1')

        self.assertEqual(actual, expected)

    def test_chop_into_lines(self):
        replacee = 'jinsung\r\nchoi\r\nsays\nhello\r\n\r\n\r\n'
        actual = src.chop_into_lines(replacee)

        expected = ['jinsung', 'choi', 'says', 'hello']

        self.assertEqual(actual, expected)

    def test_group_sentences(self):
        sentences = ['sentence1','sentence2','sentence3','sentence4','sentence5','sentence6','sentence7','sentence8','sentence9','sentence10']

        def joiner(prev, curr):
            return len(prev)<5

        actual = src.group_sentences(sentences, joiner, '\n\n', '**')
        
        expected = 'sentence1**sentence2**sentence3**sentence4**sentence5\n\nsentence6**sentence7**sentence8**sentence9**sentence10'

        self.assertEqual(actual, expected)


def load_file(filename):
    with open(filename, 'r') as fp:
        content = fp.read()
    return content


if __name__ == '__main__':
    unittest.main()
