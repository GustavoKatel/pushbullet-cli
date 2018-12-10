#!/bin/sh

set -x # debug
set -e # exit if any command fail

cd /opt/pushbullet-cli
pip install pipenv
pipenv install -d
pipenv run pytest
pipenv --rm
