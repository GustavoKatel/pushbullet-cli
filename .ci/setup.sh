#!/bin/bash

if [ "$TRAVIS_OS_NAME" == "osx" ]; then
    brew update
    brew install pyenv
    brew install pyenv-virtualenv
    pyenv install $PYTHON
    export PYENV_VERSION=$PYTHON
    export PATH="/Users/travis/.pyenv/shims:${PATH}"
    pyenv-virtualenv venv
    source venv/bin/activate
    python --version
fi
