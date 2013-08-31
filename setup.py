
from setuptools import setup

import subsample

setup(name = 'subsample',
      version = subsample.__version__,
      description = 'Command-line interface for sampling lines from text files',
      url = 'https://github.com/paulgb/subsample',
      author = 'Paul Butler',
      author_email = 'paulgb@gmail.com',
      packages = ['subsample'],
      entry_points = {
          'console_scripts': [
              'subsample = subsample.main:main'
          ]
      },
)

