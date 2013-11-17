
'''
Sample lines from text files (for example, rows of a .csv or .tsv file)
from the command line.
'''

import argparse
from sys import stderr
from itertools import chain
import logging
import random

from algorithms import reservoir_sample, approximate_sample, two_pass_sample
from file_input import FileInput

logging.basicConfig(level=logging.DEBUG, format='LOG %(asctime)s > %(message)s', datefmt='%H:%M')

DEFAULT_FRACTION = 0.01
DEFAULT_SAMPLE_SIZE = 100

PERCENT = 100


def main():
    parser = argparse.ArgumentParser(prog='subsample', description=__doc__)
    parser.add_argument('input_file', default='-',
            help='csv, tsv, or other newline-separated data file')
    parser.add_argument('--seed', '-s', type=int, default=None,
            help='random number generator seed, for reproducable results')
    parser.add_argument('--header-rows', '-r', type=int, nargs='?', const=1, default=0,
            help='number of header rows to preserve in sample')

    parser.add_argument('--percent', '-p', type=float, default=None,
            help='specify sample size as a percent of total')
    parser.add_argument('--fraction', '-f', type=float, default=None,
            help='specify sample size as a fraction of total')
    parser.add_argument('--sample-size', '-n', type=int, default=None,
            help='specify number of samples directy')

    parser.add_argument('--approximate', '-app', action='store_true',
            default=False,
            help='Use approximate algorithm. Requires sample size to be specified '+
                 'as a percent or fraction. One-pass and constant space, but sample '+
                 'size is not guaranteed to be exact.')
    parser.add_argument('--reservoir', '-res', action='store_true',
            help='Use one-pass reservoir sampling algorithm. Sample size must be fixed. '+
                 'Sample must fit in memory. Used by default if no '+
                 'other algorithm is specified.')
    parser.add_argument('--two-pass', '-tp', action='store_true',
            default=False,
            help='Use two-pass sampling algorithm. List of indices to sample must fit '+
                 'in memory.')

    args = parser.parse_args()

    if (not args.two_pass) and (not args.approximate):
        args.reservoir = True

    if args.two_pass and args.input_file == '-':
        print >> stderr, ('The two-pass algorithm does not support standard input. '
            'Use another algorithm or save to a file first.')
        exit(1)

    if args.percent is not None and args.fraction is not None:
        print >> stderr, 'If percent is specified, fraction must not be'
        exit(1)

    if args.percent is not None:
        args.fraction = args.percent / 100

    if (args.fraction is not None) and (args.sample_size is not None):
        print >> stderr, 'If sample size is specified, percent and fraction must not be.'
        exit(1)

    if (args.fraction is not None) and args.reservoir:
        print >> stderr, ('percent and fraction cannot be used with reservoir algorithm; '
            'use sample size instead.')
        exit(1)

    if (args.sample_size is not None) and args.approximate:
        print >> stderr, ('sample size cannot be given with the approximate algorithm; '
            'use fraction or percent instead.')
        exit(1)

    fi = FileInput(args.input_file, args.header_rows)

    if args.seed is not None:
        random.seed(args.seed)

    if args.approximate:
        if args.fraction is None:
            args.fraction = DEFAULT_FRACTION
        sample = approximate_sample(fi, args.fraction)

    elif args.two_pass:
        if args.fraction:
            sample = two_pass_sample(fi, fraction=args.fraction)
        else:
            if args.sample_size is None:
                args.sample_size = DEFAULT_SAMPLE_SIZE
            sample = two_pass_sample(fi, sample_size=args.sample_size)

    else:
        if args.sample_size is None:
            args.sample_size = DEFAULT_SAMPLE_SIZE
        sample = reservoir_sample(fi, args.sample_size)

    for line in chain(fi.header, sample):
        print line,


if __name__ == '__main__':
    main()

