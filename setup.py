#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of cabin-porn.
# https://github.com/RichardLitt/cabin-porn

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Richard Littauer <richard.littauer@gmail.com>

from setuptools import setup, find_packages
from cabin_porn import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='cabin-porn',
    version=__version__,
    description='Set the current desktop to a cabin from CabinPorn.com.',
    long_description='''
Set the current desktop to a cabin from CabinPorn.com.
''',
    keywords='cabin background',
    author='Richard Littauer',
    author_email='richard.littauer@gmail.com',
    url='https://github.com/RichardLitt/cabin-porn',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # add your dependencies here
        # remember to use 'package-name>=x.y.z,<x.y+1.0' notation (this way you get bugfixes)
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            # 'cabin-porn=cabin_porn.cli:main',
            'cabin-porn-it=cabin_porn.cabin:main'
        ],
    },
)
