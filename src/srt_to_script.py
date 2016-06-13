#!/usr/bin/python3

from os import linesep
import re
import sys
from html_tag_stripper import strip_tags

def read_srt_file(filename):
    with open(filename, 'r', errors='replace') as fp:
        content = fp.read()
    return content


def strip_number_counters(srt):
    pattern = re.compile(r'\d{1,} *\r?\n(\d{2}:\d{2}:\d{2},\d{3})')
    return re.sub(pattern, r'\1', srt)


def strip_time_indicator(srt):
    pattern = re.compile(r'\d{2}:\d{2}:\d{2},\d{3} *--> *\d{2}:\d{2}:\d{2},\d{3}\r?\n')
    return re.sub(pattern, '', srt)


def strip_empty_lines(srt):
    #for supporting *nix,mac,windows respectively
    pattern = re.compile('(\n|\r|\r\n){2,}')
    return re.sub(pattern, r'\1', srt)


def chop_into_lines(srt):
    return srt.strip().splitlines()


def group_sentences(lines, joiner, psep=linesep*2, lsep=' '):
    '''
    joiner is a function
        :param1 previous sentences in list; a.k.a paragraph
        :param2 current sentence
        :return True if current sentence joins current paragraph, False to make new paragraph
                with this current sentence
    psep: seperator between paragraphs
    lsep: seperator between sentences in same paragraph
    '''
    paragraphs = []
    paragraph = []

    for line in lines:
        join_or_not = joiner(paragraph, line)
        if(join_or_not == True):
            paragraph.append(line)
        else:
            paragraphs.append(paragraph)
            paragraph = [line]

    if len(paragraph)>0:
        paragraphs.append(paragraph)

    return psep.join( [lsep.join(paragraph) for paragraph in paragraphs] )


def main(infile):
    srt = read_srt_file(infile)

    srt = strip_number_counters(srt)

    srt = strip_time_indicator(srt)

    srt = strip_empty_lines(srt)

    lines = chop_into_lines(srt)

    def joiner(prev_lines, curr_line):
        accu_cnt = sum([len(line) for line in prev_lines]) + len(curr_line)
        minimum = 300
        maximum = minimum + 100

        if accu_cnt < minimum: 
            return True

        elif not ends_with_punctuation(prev_lines[-1]):
            return True

        return False

    screenplay = group_sentences(lines, joiner, linesep*2, '  ')

    screenplay = strip_tags(screenplay)

    return screenplay

def ends_with_punctuation(sentence):
    return len(sentence)>0 and sentence[-1] in '.!?'

if __name__ == '__main__':
    infile = sys.argv[1]

    screenplay = main(infile)

    print(screenplay)
