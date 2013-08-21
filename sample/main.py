
import argparse
from sys import stdin, stderr
from itertools import islice, chain
import random

DEFAULT_FRACTION = 0.01
DEFAULT_SAMPLE_SIZE = 100

PERCENT = 100

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


def reservoir_sample(rows, sample_size):
    reservoir = list(islice(rows, sample_size))
    for i, row in enumerate(rows, sample_size):
        r = random.randint(0, i)
        if r < sample_size:
            reservoir[r] = row
    return reservoir


def stochastic_sample(rows, fraction):
    for row in rows:
        if random.random() < fraction:
            yield row


def two_pass_sample(row_function, sample_size=None, fraction=None):
    population_size = sum(1 for _ in row_function())

    if fraction is not None:
        sample_size = round(population_size * fraction)
    sample = set(random.sample(xrange(population_size), sample_size))

    rows = row_function()
    def row_generator():
        for i, row in enumerate(rows):
            if i in sample:
                yield row
    return row_generator()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', nargs='?', default='-')
    parser.add_argument('--seed', '-s', type=int, default=None)
    parser.add_argument('--header-rows', '-r', type=int, default=0)

    parser.add_argument('--percent', '-p', type=float, default=None)
    parser.add_argument('--fraction', '-f', type=float, default=None)
    parser.add_argument('--sample-size', '-n', type=int, default=None)

    parser.add_argument('--stochastic', '-stoc', nargs='?', const=True, default=False)
    parser.add_argument('--reservoir', '-res', nargs='?', const=True, default=False)
    parser.add_argument('--two-pass', '-tp', nargs='?', const=True, default=False)
    args = parser.parse_args()

    fi = FileInput(args.input_file, args.header_rows)
    if args.seed is not None:
        random.seed(args.seed)

    if args.percent is not None and args.fraction is not None:
        print >> stderr, 'If percent is specified, fraction must not be'
        exit(1)

    if args.percent is not None:
        args.fraction = args.percent / 100

    if (args.fraction is not None) and (args.sample_size is not None):
        print >> stderr, 'If sample size is specified, percent and fraction must not be.'
        exit(1)

    if (args.fraction is not None) and args.reservoir:
        print >> stderr, 'percent and fraction cannot be used with reservoir algorithm; use sample size instead.'
        exit(1)

    if (args.sample_size is not None) and args.stochastic:
        print >> stderr, 'sample size cannot be given with the stochastic algorithm; use fraction or percent instead.'
        exit(1)

    if args.stochastic:
        if args.fraction is None:
            args.fraction = DEFAULT_FRACTION
        sample = stochastic_sample(fi.get_input(), args.fraction)

    elif args.two_pass:
        if args.fraction:
            sample = two_pass_sample(fi.get_input, fraction=args.fraction)
        else:
            if args.sample_size is None:
                args.sample_size = DEFAULT_SAMPLE_SIZE
            sample = two_pass_sample(fi.get_input, sample_size=args.sample_size)

    else:
        if args.sample_size is None:
            args.sample_size = DEFAULT_SAMPLE_SIZE
        sample = reservoir_sample(fi.get_input(), args.sample_size)

    for line in chain(fi.header, sample):
        print line,


if __name__ == '__main__':
    main()

