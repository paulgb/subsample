Sample
======

``sample`` is a command-line tool for sampling data from a large,
newline-separated dataset (typically a CSV-like file).

Installation
------------

``sample`` is distributed with ``pip``. Once you've installed ``pip``,
simply run::

    > pip install sample-cli

and sample will be installed into your Python environment.

Usage
-----

``sample`` requires one argument, the input file. If the input file
is ``-``, data will be read from standard input (in this case, only
the reservoir and approximate algorithms can be used).

Simple Example
**************

To take a sample of size 1000 from the file ``big_data.csv``,
run ``sample`` as follows::

    > sample -n 1000 big_data.csv

This will print 1000 random lines from the file to the terminal.

File Redirection
****************

Usually we want to save the sample to another file instead.
``sample`` doesn't have file output built-in; instead it relies
on the output redirection features of your terminal. To save
to ``big_data_sample.csv``, run the following command::

    > sample -n 1000 big_data.csv > big_data_sample.csv

Header Rows
***********

CSV files often have a header row with the column names. You can pass
the ``-r`` flag to ``sample`` to preserve the header row::

    > sample -n 1000 big_data.csv -r > big_data_sample.csv

Rarely, you may need to sample from a file with a header spanning
multiple rows. The ``-r`` argument takes an optional number of
rows to preserve as a header::

    > sample -n 1000 -r 3 data_with_header.csv > sample_with_header.csv

Note that if the ``-r`` argument is directly before the input filename,
it must have an argument or else it will try to interpret the input
filename as the number of header rows and fail. Putting the ``-r`` argument
after the input filename will avoid this.

Random Seed
***********

The output of ``sample`` is random and depend on the computer's random
state. Sometimes you may want to take a sample in a way that can be
reproduced. You can pass a random seed to ``sample`` with the ``-s`` flag
to accomplish this::

    > sample -s 45906345 data_file.csv > reproducable_sample.csv

Sampling Algorithms
-------------------

Algorithm Comparison
********************

``sample`` implements three sampling algorithms, each with their own strengths
and weaknesses.

+------------------------+----------------+----------------+------------+
|                        | Reservoir      | Approximate    | Two-pass   |
+========================+================+================+============+
| Flag                   | ``--res``      | ``--app``      | ``--tp``   |
+------------------------+----------------+----------------+------------+
| ``stdin``-compatible   | yes            | yes            | no         |
+------------------------+----------------+----------------+------------+
| space complexity       | ``O(ss * rs)`` | ``O(1)``       | ``O(ss)``  |
+------------------------+----------------+----------------+------------+
| fixed sample size      | compatible     | not compatible | compatible |
+------------------------+----------------+----------------+------------+
| fractional sample size | not compatible | compatible     | compatible |
+------------------------+----------------+----------------+------------+

For space complexity, `ss` is the number of records in the sample and `rs` is the maximum size of a record.

Reservoir Sampling
******************

Reservoir sampling (`Random Sampling with a Reservoir (Vitter 85) <http://www.mathcs.emory.edu/~cheung/papers/StreamDB/RandomSampling/1985-Vitter-Random-sampling-with-reservior.pdf>`__)
is a method of sampling from a stream of unknown size where the sample size is
fixed in advance. It is a one-pass algorithm and uses space proportional to the
amount of data in the sample.

Reservoir sampling is the default algorithm used by ``sample``. For consistency,
it can also be invoked with the argument ``--reservoir``.

If reservoir sampling, the sample size must be fixed rather than fractional.

Example::

    > sample --reservoir -n 1000 big_data.csv > sample_data.csv

Approximate Sampling
********************

Approximate sampling simply includes each row in the sample with a probability
given as the sample proportion. It is a stateless algorithm with minimal space
requirements. Samples will have on average a size of ``fraction * population_size``,
but it will vary between each invocation. Because of this, approximate sampling
is only useful when the sample size does not have to be exact (hence the name).

Example::

    > sample --approximate -f 0.15 my_data.csv > my_sample.csv

Equivalently, supply a percentage instead of a fraction by switching the
``-f`` to a ``-p``::

    > sample --approximate -p 15 my_data.csv > my_sample.csv

Two-Pass Sampling
*****************

Two-pass sampling is allowed two passes, first to count the number of records
(ie. the population size) and second to emit the records which are part of the
sample. Because of this it is not compatible with ``stdin`` as an input.

As two-pass sampling knows the population size, it will accept the sample size
as either a fraction or a fixed number of elements.

Example::

    > sample --two-pass -p 15 my_data.csv > my_sample.csv

Two-pass sampling uses memory proportional to the number of elements in the sample.
