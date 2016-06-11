#!/usr/bin/python3

import re
import sys

def read_srt_file(filename):
    with open(filename, 'r') as fp:
        content = fp.read()
    return content


def strip_number_counters(srt):
    pattern = re.compile(r'\d{1,} *\r?\n(\d{2}:\d{2}:\d{2},\d{3})')
    return re.sub(pattern, r'\1', srt)


def strip_time_indicator(srt):
    pattern = re.compile(r'\d{2}:\d{2}:\d{2},\d{3} *--> *\d{2}:\d{2}:\d{2},\d{3}\r?\n')
    return re.sub(pattern, '', srt)


def strip_empty_lines(srt):
    pattern = re.compile('(\r\n){2,}')
    return re.sub(pattern, '\r\n', srt)


def chop_into_lines(srt):
    return srt.strip().splitlines()


def group_sentences(lines, joiner, psep='\n\n', lsep=' '):
    '''
    joiner is a function
        :param1 previous sentences in list
        :param2 current sentence
        :return True if join the current to the current paragraph, False to make new paragraph
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
        return sum([len(line) for line in prev_lines]) + len(curr_line) < 300

    screenplay = group_sentences(lines, joiner, '\n\n', '  ')

    return screenplay


if __name__ == '__main__':
    infile = sys.argv[1]

    screenplay = main(infile)

    print(screenplay)
