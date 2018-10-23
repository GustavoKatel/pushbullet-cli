#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import functools
import os

from setuptools import find_packages, setup

setup(
    name="pushbullet-cli",
    description='Command line tool for controlling PushBullet',
    author='Gustavo Sampaio',
    author_email='gbritosampaio@gmail.com',
    url='https://github.com/GustavoKatel/pushbullet-cli',
    version='0.7.6',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pushbullet.py >= 0.11.0',
        'click',
        'keyring>=15.1.0',
        'keyrings.alt'
    ],
    entry_points={
        'console_scripts': ['pb = pushbullet_cli.app:main']
    },
)
