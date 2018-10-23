Contributing Guidelines
=======================

Since version v0.8 (to-be-released), *pushbullet-cli* supports python versions from 3.5 to 3.7. Dropping support to python <=2.7

You can see test information and coverage reports in `README`_

Dependencies
------------

*Pipenv* is used to manage python dependencies and virtual environment.

To install all the required tools, run:

.. code::

    $ pipenv install -d

To activate the newly created environment, run:

.. code::

    $ pipenv shell

This will spawn a new shell with the environment activated.

Important! Please remember to keep the *Pipfile* and *Pipfile.lock* in sync.

Tools
----------

We use *yapf* and * isort* to format all the code. A task ( `pyinvoke`_ ) is provided to automate this process.

.. code::

    $ inv format

Will format the necessary code with the pre-configured settings.

Also git `pre-commit`_ hooks are provided to make sure everything is in order before commiting and pushing.

You can install the hooks with:

.. code::

    $ inv install-hooks


Testing
--------

Tests are handled with pytest.

.. code::

    $ inv test [--nocov]

Will run all the tests. The flag *--nocov* will disable coverage reports.

.. _README: https://github.com/GustavoKatel/pushbullet-cli
.. _pyinvoke: http://www.pyinvoke.org/
.. _pre-commit: https://pre-commit.com
