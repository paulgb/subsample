
from sys import stdin

class FileInput(object):
    def __init__(self, filename, header_rows):
        self.filename = filename
        self.header_rows = header_rows

    def get_input(self):
        if self.filename == '-':
            fh = stdin
        else:
            fh = open(self.filename)
        self.header = list()
        for i in range(self.header_rows):
            self.header.append(fh.readline())
        return fh

