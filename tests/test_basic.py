#!/usr/bin/python3

from .context import src

import unittest

class TestBasic(unittest.TestCase):
    '''Basic test cases'''

    def test_srtentry(self):
        raw = "1\n00:00:01,123 --> 00:00:04,345\nHello Sir.\nMy name is Jin"
        entry = src.SrtEntry(raw, lsep=' ')
        
        self.assertEqual(entry.counter, "1")
        self.assertEqual(entry.time_start, "00:00:01,123")
        self.assertEqual(entry.time_stop, "00:00:04,345")
        self.assertEqual(entry.sentences, "Hello Sir. My name is Jin")

    def test_chop_into_raw_entries(self):
        replacee = load_file('./tests/sample/subtitle_short.srt')
        actual = src.chop_into_raw_entries(replacee)[:2]

        expected = ['1\n00:00:00,100 --> 00:01:52,320\nwww.TUSUBTITULO.com\n-DIFUNDE LA CULTURA-',
                    '2\n00:02:46,696 --> 00:02:48,228\nBurn them all!']

        self.assertEqual(actual, expected)

def load_file(filename):
    with open(filename, 'r') as fp:
        content = fp.read()
    return content


if __name__ == '__main__':
    unittest.main()
