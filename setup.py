#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = "Pushbullet CLI",
    version = "0.1",
    packages = find_packages(exclude=['tests']),
    install_requires=['pushbullet.py >= 0.7.1, < 0.8'],
    entry_points = {
        'console_scripts': ['pb = pushbullet_cli.app:main']
    },
)
