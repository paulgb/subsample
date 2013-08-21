
from setuptools import setup

setup(name = 'sample-cli',
      version = '0.0.1',
      description = 'Command-line interface for sampling lines from text files',
      author = 'Paul Butler',
      author_email = 'paulgb@gmail.com',
      packages = ['sample'],
      entry_points = {
          'console_scripts': [
              'sample = sample.main:main'
          ]
      },
)

