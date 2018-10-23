from __future__ import print_function, unicode_literals

import pytest


def test_list_devices_zero(list_devices, pb_api):
    result = list_devices()
    assert result.output == ''


def test_list_devices(list_devices, pb_api):
    pb_api.new_device('d1')
    pb_api.new_device('d2')
    result = list_devices()
    assert result.output == '''0. d1
1. d2
'''
