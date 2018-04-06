#!/usr/bin/env python
from setuptools import setup, find_packages
import functools
import os

setup(
    name="pushbullet-cli",
    description='Command line tool for controlling PushBullet',
    author='Roey Darwish Dror',
    author_email='roey.ghost@gmail.com',
    url='https://github.com/GustavoKatel/pushbullet-cli',
    version='0.7.6',
    packages=find_packages(exclude=['tests']),
    install_requires=['pushbullet.py >= 0.9.0', 'click', 'keyring>=8.2', 'keyrings.alt'],
    entry_points={
        'console_scripts': ['pb = pushbullet_cli.app:main']
    },
)
