from __future__ import unicode_literals

import click
import pytest
from click.testing import CliRunner


@pytest.yield_fixture
def pb_api(mocker):
    from pushbullet_cli import app
    from tests.mock_pushbullet import MockPushBullet
    mock_pb = MockPushBullet()
    with mocker.patch.object(app, '_get_pb', return_value=mock_pb):
        yield mock_pb


@pytest.fixture
def runner(pb_api):
    runner = CliRunner()
    return runner


def wrap_runner_func(runner, func):
    def invoke(arg_list=[], should_raise=True, **kwargs):
        result = runner.invoke(func, arg_list, **kwargs)
        if should_raise:
            if result.exception is not None:
                raise result.exception
            assert result.exit_code == 0
        return result

    return invoke


@pytest.fixture
def push(runner):
    from pushbullet_cli.app import push
    return wrap_runner_func(runner, push)


@pytest.fixture
def list_devices(runner):
    from pushbullet_cli.app import list_devices
    return wrap_runner_func(runner, list_devices)


@pytest.fixture
def list_pushes(runner):
    from pushbullet_cli.app import list_pushes
    return wrap_runner_func(runner, list_pushes)


@pytest.fixture
def set_key(runner):
    from pushbullet_cli.app import set_key
    return wrap_runner_func(runner, set_key)
