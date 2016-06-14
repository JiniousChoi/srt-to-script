#!/usr/bin/python3

from os import linesep
import re
import sys
from html_tag_stripper import strip_tags

LINESEP = linesep
LSEP = '  '
PSEP = '\n\n'

class SrtEntry:
    def __init__(self, raw, lsep=LSEP):
        self.lsep = lsep
        self.parse(raw)

    def parse(self, raw):
        pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*)', re.DOTALL)
        matcher = re.search(pattern, raw)
        self.counter = matcher.group(1)
        self.time_start = matcher.group(2)
        self.time_stop = matcher.group(3)
        self.sentences = self.remove_lineseps(matcher.group(4))

    def remove_lineseps(self, sentences):
        return sentences.replace('\n', self.lsep)


def read_srt_file(filename):
    with open(filename, 'r', errors='replace') as fp:
        content = fp.read()
    return content


def preprocess_linesep(raw):
    #translate windows,mac newlines into *nix-like style
    raw = raw.replace('\r\n', '\n')
    raw = raw.replace('\r', '\n')
    return raw


def chop_into_raw_entries(srt):
    srt = preprocess_linesep(srt)
    raw_entries = re.split('\n\n', srt)

    def is_legit_sentence(line):
        return line!=None and re.search(r'\S+', line)

    raw_entries = filter(is_legit_sentence, raw_entries)
    return list(raw_entries)


def make_screenplay(srt_entries, grouping_entries, make_paragraph, psep=linesep*2, lsep='  '):
    '''
    grouping_entries is a function
        :param1 previous sentences in list; a.k.a paragraph
        :param2 current sentence
        :return True if current sentence joins current paragraph, False to make new paragraph
                with this current sentence
    psep: seperator between paragraphs
    lsep: seperator between sentences in same paragraph
    '''
    groups = []
    group = [] #a group of entries to be one-paragraphed

    for srt_entry in srt_entries:
        join_or_not = grouping_entries(group, srt_entry)
        if(join_or_not == True):
            group.append(srt_entry)
        else:
            groups.append(group)
            group = [srt_entry]

    if len(group)>0:
        groups.append(group)

    screenplay = psep.join( [make_paragraph(group, lsep) for group in groups] )
    return screenplay


def main(infile):
    srt = read_srt_file(infile)

    srt = strip_tags(srt)

    raw_entries = chop_into_raw_entries(srt)

    srt_entries = [SrtEntry(raw_entry) for raw_entry in raw_entries]

    def grouping_entries(prev_entries, curr_entry):
        accu_cnt = sum([len(entry.sentences) for entry in prev_entries]) + len(curr_entry.sentences)
        minimum = 300
        maximum = minimum + 100

        if accu_cnt < minimum: 
            return True
        elif accu_cnt > maximum:
            return False
        elif ends_with_punctuation(prev_entries[-1].sentences):
            return False
        else:
            return True

    def make_paragraph(entries, lsep):
        header = entries[0].time_start
        content = lsep.join([entry.sentences for entry in entries])
        paragraph = '['+header+']' + lsep + content
        return paragraph

    screenplay = make_screenplay(srt_entries, grouping_entries, make_paragraph)

    return screenplay


def ends_with_punctuation(sentence):
    return len(sentence)>0 and sentence[-1] in '.!?'

if __name__ == '__main__':
    infile = sys.argv[1]

    screenplay = main(infile)

    print(screenplay)
