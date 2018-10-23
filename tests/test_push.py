from __future__ import print_function, unicode_literals

import pytest


def test_push_str(push, pb_api):
    result = push(['test'])

    pb_api.push_note.assert_called_once_with(body='test', title='')


def test_push_str_with_title(push, pb_api):
    result = push(['test', '-t', 'my title'])

    pb_api.push_note.assert_called_once_with(body='test', title='my title')


def test_push_not_tty(push, pb_api):
    result = push([], input='test isatty\n')
    assert not 'Enter your message:' in result.output


def test_push_invalid_device(push, pb_api):
    from pushbullet_cli.app import InvalidDevice
    result = push(['test', '-d', 0], should_raise=False)
    assert result.exit_code == 1
    assert result.output == 'Error: Invalid device number 0. Choose one of the following devices:\n\n'


def test_push_to_device(push, pb_api):
    from tests.mock_pushbullet import MockPushBullet
    device = MockPushBullet()
    pb_api.devices.append(device)
    result = push(['test', '-d', 0])
    device.push_note.assert_called_once_with(body='test', title='')
    pb_api.push_note.assert_not_called()


def test_push_to_channel(push, pb_api, mocker):
    import pushbullet
    from tests.mock_pushbullet import MockPushBullet
    channel = MockPushBullet()

    with mocker.patch.object(
            pushbullet.channel, 'Channel', return_value=channel):
        result = push(['test', '-c', 'test_channel'])
        channel.push_note.assert_called_once_with(body='test', title='')
        pb_api.push_note.assert_not_called()


def test_push_link(push, pb_api):
    link = 'https://google.com'
    result = push(['--link', link])
    pb_api.push_link.assert_called_once_with(url=link, title=link, body=None)


def test_push_link_with_title(push, pb_api):
    link = 'https://google.com'
    result = push(['--link', link, '-t', 'my title'])
    pb_api.push_link.assert_called_once_with(
        url=link, title='my title', body=None)


def test_push_file(push, pb_api, tmpdir):
    filename = tmpdir.join('burrito.txt')
    filename.write('want some burrito?')
    push(['--file', str(filename)])
    pb_api.push_file.assert_called_once_with(body=None, filename='burrito.txt')
