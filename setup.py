#!/usr/bin/env python
# encoding=utf-8
from __future__ import print_function
import os
import sys

try:
    from setuptools import setup
except ImportError:
    print("This package requires 'setuptools' to be installed.")
    sys.exit(1)


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(name='otsrdflib',
      version='0.1.0',
      description='Ordered Turtle Serializer for rdflib',
      long_description=README,
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4'
      ],
      keywords='rdflib turtle serializer',
      author='Dan Michael O. Heggø',
      author_email='danmichaelo@gmail.com',
      url='https://github.com/scriptotek/rdflib_ots',
      license='MIT',
      packages=['otsrdflib'],
      install_requires=['rdflib'],
      zip_safe=True
      )
