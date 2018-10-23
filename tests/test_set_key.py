from __future__ import print_function, unicode_literals

import pytest


def test_set_key(set_key, pb_api, mocker):
    import keyring
    import getpass
    prev_token = keyring.get_password("pushbullet", "cli")
    try:
        with mocker.patch.object(getpass, 'getpass', return_value='abc'):
            set_key()
            assert keyring.get_password("pushbullet", "cli") == 'abc'
    finally:
        keyring.set_password("pushbullet", "cli", prev_token)
