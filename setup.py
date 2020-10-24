#!/usr/bin/env python
import functools
import os

from setuptools import find_packages, setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name="pushbullet-cli",
    description='Command line tool for controlling PushBullet',
    long_description=readme(),
    author='Gustavo Sampaio',
    author_email='gbritosampaio@gmail.com',
    url='https://github.com/GustavoKatel/pushbullet-cli',
    version='1.1',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pushbullet.py>=0.11,<0.13', 'click~=7.0', 'keyring~=21.3.0',
        'keyrings.alt~=3.1'
    ],
    entry_points={'console_scripts': ['pb = pushbullet_cli.app:main']},
)
