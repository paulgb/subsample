
from setuptools import setup

import sample

setup(name = 'sample-cli',
      version = sample.__version__,
      description = 'Command-line interface for sampling lines from text files',
      url = 'https://github.com/paulgb/sample',
      author = 'Paul Butler',
      author_email = 'paulgb@gmail.com',
      packages = ['sample'],
      entry_points = {
          'console_scripts': [
              'sample = sample.main:main'
          ]
      },
)

