#!/usr/bin/env python3
# coding: utf-8

import argparse

def make_struct(**kw):
    return argparse.Namespace(**kw)

if __name__ == "__main__":
    fpath = "~/opt/programming/pdf/adobe_supplement_iso32000.pdf"
    
    # :TRICKY: io.open(newline='') воспримет любые 
    # окончания строк, но не работает с бинарным режимом "rb"
    #import io
    #with io.open(fpath, 'rb', newline='') as f:

    import re
    # без (?!) очень сложная регулярка получается, вроде
    #eol = re.compile(br'(?:(\r)[^\n]|\Z)|(\r?\n)')
    eol = re.compile(br'(\r(?!\n))|(\r?\n)')
    assert eol.search(b"\r").end() == 1
    assert eol.search(b"\ra").end() == 1
    assert eol.search(b"\r\n").end() == 2
    assert eol.search(b"\n\r").end() == 1
    
    
    # построчный разбор в бинарном файле, так как в 
    # Python3.4 разбор по универсальным строкам при io.open(mode='rb', newline='')
    # не работает
    # :TRICKY: сейчас последняя пустая строка не выдается (т.е. в случае наличия \n 
    # в конце; если потребуется, то необходимо вводить флаг trailing_empty = False
    # для таких случаев)
    def make_fbr(f):
        return make_struct(
            f   = f,
            buf = b"", 
            may_read = True
        )
    
    BUF_SIZE = 4096
    def next_line(fbr):
        buf = fbr.buf
        line = None
        while True:
            m = eol.search(buf)
            found = bool(m)
            if found:
                beg, end = m.span()
                if end == len(buf) and buf[-1] == "\r" and fbr.may_read:
                    found = False
                else:
                    line = buf[:beg]
                    buf  = buf[end:]
                    break

            if not found and fbr.may_read:
                tail = fbr.f.read(BUF_SIZE)
                fbr.may_read = bool(tail)
                buf += tail
            else:
                if buf:
                    line = buf
                    buf = b''
                break

        fbr.buf = buf
        return line
        
    def print_lines(f):
        fbr = make_fbr(f)
        line = next_line(fbr)
        
        while line is not None:
            print(line)
            line = next_line(fbr)
    
    import io
    print_lines(open("~/opt/programming/pdf/tmp/ggg", "br"))
    
    #with open(fpath, 'rb') as f:
        ##head = f.readline()

        #assert head == b'%PDF-1.'
        #print(head)