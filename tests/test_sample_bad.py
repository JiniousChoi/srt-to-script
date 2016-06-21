#!/usr/bin/python3

from .context import src

import unittest

class SampleBadTest(unittest.TestCase):
    '''Given sample is a bit corrupted.'''

    def test_chop_into_raw_entries(self):
        '''first line does not have dialog'''
        replacee = "\ufeff1\n00:00:00,000 --> 00:00:02,350\n\n\n2\n00:00:02,350 --> 00:00:06,369\nMALE SPEAKER: Thank you for\ncoming to Edmond Lau's talk.\n\n3\n00:00:06,370 --> 00:00:10,790\nHe will be talking about how to\nbe a more effective engineer.\n\n\n"

        expected = ['\ufeff1\n00:00:00,000 --> 00:00:02,350',
                    "2\n00:00:02,350 --> 00:00:06,369\nMALE SPEAKER: Thank you for\ncoming to Edmond Lau's talk.",
                    '3\n00:00:06,370 --> 00:00:10,790\nHe will be talking about how to\nbe a more effective engineer.']

        actual = src.chop_into_raw_entries(replacee)

        self.assertEqual(actual, expected)

def load_file(filename):
    with open(filename, 'r') as fp:
        content = fp.read()
    return content


if __name__ == '__main__':
    unittest.main()
