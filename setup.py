#!/usr/bin/env python
import functools
import os

from setuptools import find_packages, setup


def readme():
    with open("README.rst") as f:
        return f.read()


def reqs():
    with open("requirements.txt") as f:
        return f.readlines()


def version():
    with open("pushbullet_cli/__version__.py") as f:
        return f.read().split('"')[1]


setup(
    name="pushbullet-cli",
    description="Command line tool for controlling PushBullet",
    long_description=readme(),
    author="Gustavo Sampaio",
    author_email="gbritosampaio@gmail.com",
    url="https://github.com/GustavoKatel/pushbullet-cli",
    version=version(),
    packages=find_packages(exclude=["tests"]),
    install_requires=reqs(),
    entry_points={"console_scripts": ["pb = pushbullet_cli.app:main"]},
)
