#!/usr/bin/env python
import datetime
import getpass
import os
import os.path
import sys

import click
import keyring
import keyrings.alt
import keyrings.alt.file
import pushbullet

from .__version__ import __version__


class NoApiKey(click.ClickException):
    exit_code = 1

    def __init__(self):
        msg = (
            "No API key was specified. Either run pb set-key to set a permanent key or pass the desired key in PUSHBULLET_KEY environment vaiable.\n"
            "You can find your key at <https://www.pushbullet.com/account>."
        )
        super(NoApiKey, self).__init__(msg)


class InvalidDevice(click.ClickException):
    exit_code = 1

    def __init__(self, index, devices):
        super(InvalidDevice, self).__init__(
            "Invalid device number {0}. Choose one of the following devices:\n{1}".format(
                index,
                "\n".join(
                    "{0}. {1}".format(i, device.nickname)
                    for i, device in enumerate(devices)
                ),
            )
        )


def _get_pb():
    if "PUSHBULLET_KEY" in os.environ:
        return pushbullet.PushBullet(os.environ["PUSHBULLET_KEY"])

    password = keyring.get_password("pushbullet", "cli")
    if not password:
        raise NoApiKey()

    return pushbullet.PushBullet(password)


def _push(
    data_type,
    title=None,
    message=None,
    channel=None,
    device=None,
    file_path=None,
    url=None,
):
    pb = _get_pb()

    data = {"body": message}
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
        pb = pushbullet.channel.Channel(pb, {"tag": channel})

    if data_type == "file":
        pb.push_file(**data)
    elif data_type == "url":
        pb.push_link(title=title or url, url=url, **data)
    elif data_type == "text":
        pb.push_note(title=title if title is not None else "", **data)
    else:
        raise Exception("Unknown data type")


@click.group()
def main():
    # The pycrypto encrypted keyring asks for a password in every launch. This is unacceptable.
    if isinstance(keyring.get_keyring(), keyrings.alt.file.EncryptedKeyring):
        keyring.set_keyring(keyrings.alt.file.PlaintextKeyring())


@main.command("purge", help="Delete all your pushes.")
def purge():
    pb = _get_pb()
    pb.delete_pushes()


@main.command("dismiss", help="Mark all your pushes as read.")
def dismiss():
    pb = _get_pb()

    pushes = pb.get_pushes(filter_inactive=True)
    for current_push in pushes:
        pb.dismiss_push(current_push["iden"])


@main.command("list-devices", help="List your devices.")
def list_devices():
    pb = _get_pb()
    for i, device in enumerate(pb.devices):
        print(u"{0}. {1}".format(i, device.nickname))


@main.command("set-key", help="Set your API key.")
def set_key():
    key = getpass.getpass(
        "Enter your security token from https://www.pushbullet.com/account: "
    )
    keyring.set_password("pushbullet", "cli", key)


@main.command("delete-key", help="Remove your API key from the system keyring.")
def delete_key():
    keyring.delete_password("pushbullet", "cli")


@main.command("sms", help="Send an SMS.")
@click.option(
    "-d",
    "--device",
    type=int,
    default=None,
    required=True,
    help="Device index to send SMS from. Use pb list-devices to get the indices.",
)
@click.option(
    "-n",
    "--number",
    type=str,
    default=None,
    required=True,
    help="The phone number to send the SMS to.",
)
@click.argument("message", default=None, required=False)
def sms(device, number, message):
    pb = _get_pb()
    try:
        device = pb.devices[device]
    except IndexError:
        raise InvalidDevice(device, pb.devices)

    kwargs = {"device": device, "number": number, "message": message}
    pb.push_sms(**kwargs)


def _format_push(p):
    s = "Created:\t{}\n".format(
        datetime.datetime.fromtimestamp(p["created"]).strftime("%x %X")
    )

    s += "Sender:\t\t{}".format(p["sender_name"])
    if "sender_email" in p:
        s += " ({})".format(p["sender_email"])
    s += "\n"

    if p["type"] == "file":
        s += "Filetype:\t{}\n".format(p["file_type"])
        s += "Filename:\t{}\n".format(p["file_name"])
        s += "Link:\t\t{}\n".format(p["file_url"])
    else:
        if "title" in p:
            s += "Title:\t\t{}\n".format(p["title"])
        if "url" in p:
            s += "Link:\t\t{}\n".format(p["url"])
        if "body" in p:
            s += "\n{}\n".format(p["body"].rstrip())

    return s.rstrip()


@main.command("list", help="List your pushes.")
@click.option("-c", "--count", type=int, default=10, help="Number of pushes to fetch.")
def list_pushes(count):
    pb = _get_pb()

    pushes = pb.get_pushes(limit=count)
    print(("\n" + "-" * 50 + "\n").join(_format_push(p) for p in pushes))


@main.command(help="Push something.")
@click.option(
    "-d",
    "--device",
    type=int,
    default=None,
    help="Device index to push to. Use pb list-devices to get the indices.",
)
@click.option("-c", "--channel", type=str, default=None, help="Push to a channel.")
@click.option("-t", "--title", type=str, default=None, help="Set a title.")
@click.option(
    "-f",
    "--file",
    "filename",
    default=None,
    help="The given argument is a name file to push.",
)
@click.option("-u", "--link", default=None, help="The given argument URL.")
@click.argument("arg", default=None, required=False)
def push(title, device, channel, filename, link, arg):
    if device is not None and channel is not None:
        raise click.ClickException("--channel and --device cannot be used together")

    kwargs = {"title": title, "device": device, "channel": channel, "message": arg}

    if filename and link:
        raise click.ClickException("--file and --link cannot be used together")

    elif filename:
        kwargs["file_path"] = filename
        kwargs["data_type"] = "file"
    elif link:
        kwargs["url"] = link
        kwargs["data_type"] = "url"
    else:
        if arg is None:
            if sys.stdin.isatty():
                print("Enter your message: ")
            kwargs["message"] = sys.stdin.read()

        kwargs["data_type"] = "text"

    _push(**kwargs)


@main.command(help="Print version number.")
def version():
    print("PushBullet CLI, version " + __version__)
