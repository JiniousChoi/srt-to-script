#!/usr/bin/python3

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.fed_data = []

    def handle_data(self, data):
        self.fed_data.append(data)

    def get_data(self):
        return ''.join(self.fed_data)

def strip_tags(html):
    s = MyHTMLParser()
    s.feed(html)
    return s.get_data()
