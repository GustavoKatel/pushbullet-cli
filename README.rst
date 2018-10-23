Pushbullet CLI interface
========================

|Build Status| |Codecov| |PyPI| |license|

Installation
------------

::

   $ pip install pushbullet-cli

Usage
-----

Use `Pushbullet <https://www.pushbullet.com/>`__ from the command line.

First of all, set your API key by running:

::

   $ pb set-key

Then pasting your API key at the prompt.

Push stdin to all devices:

::

   $ echo "hello" | pb push

Push text to all devices:

::

   $ pb push "I love burritos"

Pick a device to push to:

::

   $ pb list-devices
   # Find the index of your desired device
   $ pb push -d 0 "iPhones cannot eat burritos"

Push links:

::

   $ pb push --link https://www.pushbullet.com/

Push files:

::

   $ pb push --file /path/to/burrito_photo.jpg

Push to all subscribers of channel:

::

   $ pb push -c "CHANNEL" "Why burritos are better than tacos"

Send an SMS:

::

   $ pb sms -d 0 -n +123456789 "I sense a soul in search of answers"

List your pushes:

::

   $ pb list -c 20

To set the API key from within python:

::

   import keyring, keyrings.alt
   if isinstance(keyring.get_keyring(), keyrings.alt.file.EncryptedKeyring):
       keyring.set_keyring(keyrings.alt.file.PlaintextKeyring())
   keyring.set_password("pushbullet", "cli", PUSHBULLET_KEY)

Changelog
---------

* 0.8 (WIP)

  - Remove Python 2.7 support (`Countdown <https://pythonclock.org/>`__)

  - Support to Click 7.0

  - Add test cases

  - Add travis build

  - Add coverage report

* 0.7.6

  - List previous pushes (#35)

  - Avoid prompt the user when message is piped (#34)

  - Removes default title (``Note``) (#36)

Contribution
------------

Many thanks to the original author @r-darwish

Pull requests are welcome

Take a look at the `Contributing
guidelines <https://github.com/GustavoKatel/pushbullet-cli/blob/master/CONTRIBUTING.rst>`__

.. |Build Status| image:: https://travis-ci.com/GustavoKatel/pushbullet-cli.svg?branch=master
   :target: https://travis-ci.com/GustavoKatel/pushbullet-cli
.. |Codecov| image:: https://img.shields.io/codecov/c/github/GustavoKatel/pushbullet-cli.svg
   :target: https://codecov.io/gh/GustavoKatel/pushbullet-cli
.. |PyPI| image:: https://img.shields.io/pypi/v/pushbullet-cli.svg
   :target: https://pypi.python.org/pypi/pushbullet-cli
.. |license| image:: https://img.shields.io/github/license/GustavoKatel/pushbullet-cli.svg
   :target: https://img.shields.io/github/license/GustavoKatel/pushbullet-cli.svg