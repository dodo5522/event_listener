#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from setuptools import setup, find_packages


def readme():
    try:
        _r = os.path.join(os.path.dirname(__file__), 'README.rst')
        with open(_r, 'r') as _f:
            return _f.read()
    except:
        return ''


def requires():
    try:
        with open('requirements.txt', 'r') as _f:
            return _f.readlines()
    except:
        return []


setup(
    name='event_listener',
    version='1.0.2',
    description='event listener module for solar/radiation monitor.',
    long_description=readme(),
    license="Apache Software License",
    author='Takashi Ando',
    url='https://github.com/dodo5522/event_listener.git',
    install_requires=requires(),
    packages=find_packages(),
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: Japanese',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Monitoring',
    ]
)
