#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="pushbullet-cli",
    description='Command line tool for controlling PushBullet',
    author='Roey Darwish Dror',
    author_email='roey.ghost@gmail.com',
    url='https://github.com/r-darwish/pushbullet-cli',
    version="0.1",
    packages=find_packages(exclude=['tests']),
    install_requires=['pushbullet.py >= 0.8.1'],
    entry_points={
        'console_scripts': ['pb = pushbullet_cli.app:main']
    },
)
