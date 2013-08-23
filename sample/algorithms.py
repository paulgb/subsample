
from itertools import islice
import random

def reservoir_sample(rows, sample_size):
    '''
    Reservoir sampling algorithm (see Random Sampling
    With a Reservoir, Vitter 85)

    One-pass; entire sample must fit in memory
    '''
    reservoir = list(islice(rows, sample_size))
    for i, row in enumerate(rows, sample_size):
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
        if random.random() < fraction:
            yield row


def two_pass_sample(row_function, sample_size=None, fraction=None):
    '''
    Make two passes at the data. The first pass determines the
    size. Then a set of sample_size indices pointing to the data
    is created. In the second pass, rows which match the set are
    emitted.
    '''
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

