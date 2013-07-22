#!/usr/bin/env python

from hanzo.warctools import WarcRecord
import re


def add_header(headers, line):
    map = {
           'Date': 'WARC-Date',
           'URL':  'WARC-Target-URI',
          }
    key, val = re.split(':\s*', line, 1)
    if key in map:
        key = map[key]
    headers.append( (key, val.strip()) )


def get_wb_record(filename):
    fh = open(filename)
    webbase_header = "==P=>>>>=i===<<<<=T===>=A===<=!Junghoo!==>"
    content = ''
    headers = [
                ('WARC-Filename', filename),
                ('WARC-Type', 'response'),
              ]
    finished_headers = False
    first_line = fh.readline()
    assert first_line.startswith(webbase_header)
    for line in fh:
        if line.startswith(webbase_header):
            yield headers, ('text/html', content)
            content = ''
        else:
            if finished_headers:
                content += line
            elif '' == line.strip():
                finished_headers = True
            else:
                add_header(headers, line)


i = 0
warc_out = open('out.warc.gz', 'w')
for headers, content in get_wb_record('2pages'):
    print i
    i+=1
    #print headers
    #print content
    record = WarcRecord(headers=headers, content=content)
    record.write_to(warc_out, gzip=True)
    record.dump()
    print '_'*80
