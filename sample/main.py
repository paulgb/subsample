
import argparse
from sys import stdin
from itertools import islice, chain
import random

# TODO: stochastic sampling
# TODO: two-pass sampling

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
        for line in fh:
            yield line


def resivoir_sampler(rows, sample_size):
    sample = list(islice(rows, sample_size))
    for i, row in enumerate(rows, sample_size):
        r = random.randint(0, i)
        if r < sample_size:
            sample[r] = row
    return sample


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', nargs='?', default='-')
    parser.add_argument('--sample-size', '-n', type=int, default=100)
    parser.add_argument('--header-rows', '-r', type=int, default=0)
    parser.add_argument('--seed', '-s', type=int, default=None)
    args = parser.parse_args()

    fi = FileInput(args.input_file, args.header_rows)

    if args.seed is not None:
        random.seed(args.seed)

    sample = resivoir_sampler(fi.get_input(), args.sample_size)

    for line in chain(fi.header, sample):
        print line,


if __name__ == '__main__':
    main()

