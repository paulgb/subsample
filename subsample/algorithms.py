
from itertools import islice
import random

import logging

def reservoir_sample(rows, sample_size):
    '''
    Reservoir sampling algorithm (see Random Sampling
    With a Reservoir, Vitter 85)

    One-pass; entire sample must fit in memory
    '''

    # initialize the reservoir with the first sample_size items
    reservoir = list(islice(rows, sample_size))

    for i, row in enumerate(rows, sample_size):
        # for each item, choose whether it becomes part of the
        # reservoir with decreasing probability
        r = random.randint(0, i)
        if r < sample_size:
            reservoir[r] = row

    return reservoir


def approximate_sample(rows, fraction):
    '''
    Approximate random sampling algorithm.

    Picks each row with probability given as fraction.
    This means the number of rows will be approximately
    fraction * len(rows), but will vary between runs
    with different random state.

    One pass; constant space
    '''

    for row in rows:
        # for each element, choose with probability given
        # by (fraction) whether it should be part of the sample
        if random.random() < fraction:
            yield row


def two_pass_sample(rows, sample_size=None, fraction=None):
    '''
    Make two passes at the data. The first pass determines the
    size. In the second pass, rows which are part of the sample
    are emitted.
    '''
    population_size = sum(1 for _ in rows)

    for row in rows:
        # choose 
        if random.randint(0, population_size - 1) < sample_size:
            yield row
            sample_size -= 1
        population_size -= 1


