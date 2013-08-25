
from sys import stdin
import logging

class FileInput(object):
    def __init__(self, filename, header_rows):
        self.filename = filename
        self.header_rows = header_rows

        if self.filename == '-':
            self.fh = stdin
        else:
            self.fh = open(self.filename)

        self.header = list()
        for i in range(self.header_rows):
            self.header.append(self.fh.readline())

        try:
            logging.info('Data begins at %s', self.fh.tell())
            self.data_begin = self.fh.tell()
        except IOError:
            self.data_begin = None

        self.needs_seek = False

    def __iter__(self):
        if self.needs_seek:
            self.fh.seek(self.data_begin)
        self.needs_seek = True
        return self.fh

