#!/usr/bin/env python
from setuptools import setup, find_packages
import functools
import os

_in_same_dir = functools.partial(os.path.join, os.path.dirname(__file__))

with open(_in_same_dir("pushbullet_cli", "__version__.py")) as version_file:
    exec(version_file.read())  # pylint: disable=W0122


setup(
    name="pushbullet-cli",
    description='Command line tool for controlling PushBullet',
    author='Roey Darwish Dror',
    author_email='roey.ghost@gmail.com',
    url='https://github.com/r-darwish/pushbullet-cli',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    install_requires=['pushbullet.py >= 0.9.0', 'click', 'keyring'],
    entry_points={
        'console_scripts': ['pb = pushbullet_cli.app:main']
    },
)
