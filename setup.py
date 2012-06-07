#!/usr/bin/env python

from setuptools import setup, find_packages
import sys

from eulcm import __version__

LONG_DESCRIPTION = None
try:
    # read the description if it's there
    with open('README.rst') as desc_f:
        LONG_DESCRIPTION = desc_f.read()
except:
    pass

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


setup(
    name='eulcm',
    version=__version__,
    author='Emory University Libraries',
    author_email='libsysdev-l@listserv.cc.emory.edu',
    url='https://github.com/emory-libraries/eulcm',
    license='Apache License, Version 2.0',
    packages=find_packages(),
    install_requires=['eulxml', 'eulfedora'],
    description='Python objects for Fedora Commons digital object types and related XML datastreams',
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
)
