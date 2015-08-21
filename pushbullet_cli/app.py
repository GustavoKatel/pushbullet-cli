#!/usr/bin/env python

import click
import getpass
import os
import os.path
import keyring
import pushbullet
import sys
from functools import wraps
from .__version__ import __version__


def _decode(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs).decode("ASCII")

    return wrapper

pushbullet.pushbullet.get_file_type = _decode(pushbullet.pushbullet.get_file_type)


class NoApiKey(click.ClickException):
    exit_code = 1

    def __init__(self):
        msg = ("No API key was specified. Either run pb set_key to set a permanent key or pass the desired key in PUSHBULLET_KEY environment vaiable.\n"
               "You can find your key at <https://www.pushbullet.com/account>.")
        super(NoApiKey, self).__init__(msg)


class InvalidDevice(click.ClickException):
    exit_code = 1

    def __init__(self, index, devices):
        super(InvalidDevice, self).__init__("Invalid device number {0}. Choose one of the following devices:\n{1}".format(
            index, "\n".join("{0}. {1}".format(i, device.nickname) for i, device in enumerate(devices))))


def _get_pb():
    if 'PUSHBULLET_KEY' in os.environ:
        return pushbullet.PushBullet(os.environ['PUSHBULLET_KEY'])

    password = keyring.get_password("pushbullet", "cli")
    if not password:
        raise NoApiKey()

    return pushbullet.PushBullet(password)


def _push(data_type, title=None, message=None, channel=None, device=None, file_path=None):
    pb = _get_pb()

    data = {}
    if device is not None:
        try:
            pb = pb.devices[device]
        except IndexError:
            raise InvalidDevice(device, pb.devices)

    # upload file if necessary
    if data_type == "file":
        with open(file_path, "rb") as f:
            file_data = pb.upload_file(f, os.path.basename(file_path))

        data.update(file_data)

    if channel is not None:
        pb = pushbullet.channel.Channel(pb, {'tag': channel })

    if data_type == "file":
        pb.push_file(**data)
    elif data_type == "url":
        pb.push_link(title=title or message, url=message, **data)
    elif data_type == "text":
        pb.push_note(title=title or "Note", body=message, **data)
    else:
        raise Exception("Unknown data type")


@click.group()
def main():
    pass


@main.command("purge", help="Delete all your pushes.")
def purge():
    pb = _get_pb()

    pushes = pb.get_pushes()
    for current_push in pushes[1]:
        if current_push['active']:
            pb.delete_push(current_push['iden'])


@main.command("dismiss", help="Mark all your pushes as read")
def dismiss():
    pb = _get_pb()

    pushes = pb.get_pushes()
    for current_push in pushes[1]:
        if current_push['active'] and not current_push['dismissed']:
            pb.dismiss_push(current_push['iden'])


@main.command("list-devices", help="List your devices")
def list_devices():
    pb = _get_pb()
    for i, device in enumerate(pb.devices):
        print("{0}. {1}".format(i, device.nickname))


@main.command("set-key", help="Set your API key.")
def set_key():
    key = getpass.getpass("Enter your security token from https://www.pushbullet.com/account: ")
    keyring.set_password("pushbullet", "cli", key)


@main.command("delete-key", help="Remove your API key from the system keyring")
def delete_key():
    keyring.delete_password("pushbullet", "cli")


@main.command(help="Push something.")
@click.option("-d", "--device", type=int, default=None, help="Device index to push to. Use pb list-devices to get the indices")
@click.option("-c", "--channel", type=str, default=None, help="Push to a channel.")
@click.option("-t", "--title", type=str, default=None, help="Set a title.")
@click.option("-f", "--file", "--filename", is_flag=True, help="The given argument is a name file to push")
@click.option("-u", "--link", is_flag=True, help="The given argument URL")
@click.argument('arg', default=None, required=False)
def push(title, device, channel, filename, link, arg):
    if device is not None and channel is not None:
        raise click.ClickException("--channel and --device cannot be used together")

    kwargs = {
        'title': title,
        'device': device,
        'channel': channel,
    }
    if filename and link:
        raise click.ClickException("--file and --link cannot be used together")
    elif filename:
        kwargs['file_path'] = arg
        kwargs['data_type'] = 'file'
    elif link:
        kwargs['message'] = arg
        kwargs['data_type'] = 'url'
    else:
        if arg is None:
            print("Enter your message: ")
            arg = sys.stdin.read()

        kwargs['message'] = arg
        kwargs['data_type'] = 'text'

    _push(**kwargs)


@main.command(help="Print version number.")
def version():
    print("PushBullet CLI, version " + __version__)
