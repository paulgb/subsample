Subsample
=========

``subsample`` is a command-line tool for sampling data from a large,
newline-separated dataset (typically a CSV-like file).

Installation
------------

``subsample`` is distributed with ``pip``. Once you've installed ``pip``,
simply run::

    > pip install subsample

and ``subsample`` will be installed into your Python environment.

Usage
-----

``subsample`` requires one argument, the input file. If the input file
is ``-``, data will be read from standard input (in this case, only
the reservoir and approximate algorithms can be used).

Simple Example
**************

To take a sample of size 1000 from the file ``big_data.csv``,
run ``subsample`` as follows::

    > subsample -n 1000 big_data.csv

This will print 1000 random lines from the file to the terminal.

File Redirection
****************

Usually we want to save the sample to another file instead.
``subsample`` doesn't have file output built-in; instead it relies
on the output redirection features of your terminal. To save
to ``big_data_sample.csv``, run the following command::

    > subsample -n 1000 big_data.csv > big_data_sample.csv

Header Rows
***********

CSV files often have a header row with the column names. You can pass
the ``-r`` flag to ``subsample`` to preserve the header row::

    > subsample -n 1000 big_data.csv -r > big_data_sample.csv

Rarely, you may need to sample from a file with a header spanning
multiple rows. The ``-r`` argument takes an optional number of
rows to preserve as a header::

    > subsample -n 1000 -r 3 data_with_header.csv > sample_with_header.csv

Note that if the ``-r`` argument is directly before the input filename,
it must have an argument or else it will try to interpret the input
filename as the number of header rows and fail. Putting the ``-r`` argument
after the input filename will avoid this.

Random Seed
***********

The output of ``subsample`` is random and depend on the computer's random
state. Sometimes you may want to take a sample in a way that can be
reproduced. You can pass a random seed to ``subsample`` with the ``-s`` flag
to accomplish this::

    > subsample -s 45906345 data_file.csv > reproducable_sample.csv

Sampling Algorithms
-------------------

Algorithm Comparison
********************

``subsample`` implements three sampling algorithms, each with their own strengths
and weaknesses.

+------------------------+----------------+----------------+------------+
|                        | Reservoir      | Approximate    | Two-pass   |
+========================+================+================+============+
| flag                   | ``-res``       | ``-app``       | ``-tp``    |
+------------------------+----------------+----------------+------------+
| ``stdin``-compatible   | yes            | yes            | no         |
+------------------------+----------------+----------------+------------+
| space complexity       | ``O(ss*rs)``   | ``O(1)``       | ``O(1)``   |
+------------------------+----------------+----------------+------------+
| fixed sample size      | compatible     | not compatible | compatible |
+------------------------+----------------+----------------+------------+
| fractional sample size | not compatible | compatible     | compatible |
+------------------------+----------------+----------------+------------+

For space complexity, ``ss`` is the number of records in the sample and
``rs`` is the maximum size of a record.

Reservoir Sampling
******************

Reservoir sampling (`Random Sampling with a Reservoir (Vitter 85)
<http://www.mathcs.emory.edu/~cheung/papers/StreamDB/RandomSampling/1985-Vitter-Random-sampling-with-reservior.pdf>`__)
is a method of sampling from a stream of unknown size where the sample size is
fixed in advance. It is a one-pass algorithm and uses space proportional to the
amount of data in the sample.

Reservoir sampling is the default algorithm used by ``subsample``. For consistency,
it can also be invoked with the argument ``--reservoir``.

When using reservoir sampling, the sample size must be fixed rather than fractional.

Example::

    > subsample --reservoir -n 1000 big_data.csv > sample_data.csv

Approximate Sampling
********************

Approximate sampling simply includes each row in the sample with a probability
given as the sample proportion. It is a stateless algorithm with minimal space
requirements. Samples will have on average a size of ``fraction * population_size``,
but it will vary between each invocation. Because of this, approximate sampling
is only useful when the sample size does not have to be exact (hence the name).

Example::

    > subsample --approximate -f 0.15 my_data.csv > my_sample.csv

Equivalently, supply a percentage instead of a fraction by switching the
``-f`` to a ``-p``::

    > subsample --approximate -p 15 my_data.csv > my_sample.csv

Two-Pass Sampling
*****************

As the name implies, two-pass sampling uses two passes: the first is to count the
number of records (ie. the population size) and the second is to emit the records
which are part of the sample. Because of this it is not compatible with ``stdin``
as an input.

Example::

    > subsample --two-pass -n 1000 my_data.csv > my_sample.csv

Two-pass sampling also accepts the sample size as a fraction or percent::

    > subsample --two-pass -p 15 my_data.csv > my_sample.csv

Tests
-----

A simple GNU Make-driven testing script is included. Run ``make test`` from
``subsample``'s base directory after installing to run some regression tests.

Due to the randomness inherent to random sampling, testing is limited to
checking that the output is the same when the random seed is unchanged.
This serves mainly to find new bugs introduced by changes in the future and
does not imply that the code itself is correct (in the sense that the sample
is truly random).

