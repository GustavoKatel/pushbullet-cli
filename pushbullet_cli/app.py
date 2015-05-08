#!/usr/bin/env python

import argparse
import os
import os.path
from pushbullet import PushBullet
import re
import sys
from contextlib import contextmanager
from ._compat import read_line


KEY_PATH = os.path.expanduser("~/.pushbulletkey")
URL_RE = re.compile(r"^[a-zA-Z]+://.+$")


@contextmanager
def private_files():
    oldmask = os.umask(0o77)
    try:
        yield
    finally:
        os.umask(oldmask)


def _parse_args():
    parser = argparse.ArgumentParser(description="Pushbullet")
    parser.add_argument("msg", metavar="message", nargs="*")

    devgroup = parser.add_mutually_exclusive_group()
    devgroup.add_argument("-a", "--all", default=False, action="store_true",
                          help="Push to all devices")
    devgroup.add_argument("-i", "--interactive", default=False,
                          action="store_true",
                          help="Interactively ask for device to push to")
    devgroup.add_argument("-d", "--device", type=str, default=None,
                          help="Device name to push to")
    devgroup.add_argument("-c", "--channel", type=str, default=None,
                          help="Channel name to push to")

    return parser.parse_args()


def _get_api_key():
    if not os.path.isfile(KEY_PATH):
        print("What's your API key?")
        print("Find it at <https://www.pushbullet.com/account>.")
        api_key = read_line("> ").strip()
        with private_files(), open(KEY_PATH, "w") as api_file:
            api_file.write(api_key)

        return api_key
    else:
        with open(KEY_PATH, "r") as api_file:
            return api_file.readline().rstrip()


def _prompt_device(devices):
    for i, device in enumerate(devices):
        print("[{0}] {1}".format(i, device.nickname))

    while True:
        input = raw_input("Push to which device? ").strip()
        try:
            choice = int(input)
        except (ValueError, IndexError):
            pass
        else:
            if 0 <= choice < len(devices):
                return devices[choice]


def _push(pb, channel, device, raw_data, data_type):
    data = {}
    if device is not None:
        data["device"] = device

    # upload file if necessary
    if data_type == "file":
        with open(raw_data, "rb") as f:
            file_data = pb.upload_file(f, raw_data)
            
        data.update(file_data)

    if channel is not None:
        pb = channel

    if data_type == "file":
        pb.push_file(**data)
    elif data_type == "url":
        pb.push_link(title=raw_data, url=raw_data, **data)
    else:
        pb.push_note(title="Note", body=raw_data, **data)


def _data_type(argument):
    if os.path.isfile(argument):
        return "file"
    elif URL_RE.search(argument):
        return "url"
    else:
        return "text"


def main():
    device = None
    channel = None
    args = _parse_args()

    api_key = _get_api_key()
    pb = PushBullet(api_key)

    if not args.all:
        if len(pb.devices) < 1:
            print("You don't have any devices!")
            print("Add one at <https://www.pushbullet.com/>.")
            return 1

        if args.interactive:
            device = _prompt_device(pb.devices)
        elif args.device:
            devices_by_names = {d.nickname: d for d in pb.devices}
            if args.device not in devices_by_names:
                print("Unknown device %s. Available devices: %s" % (
                    args.device, ", ".join(devices_by_names)))
                return 1
            device = devices_by_names[args.device]
        elif args.channel:
            channels_by_names = {d.channel_tag: d for d in pb.channels}
            if args.channel not in channels_by_names:
                print("Unknown channel %s. Available channels: %s" % (
                    args.channel, ", ".join(channels_by_names)))
                return 1
            channel = channels_by_names[args.channel]

    if not args.msg:
        print("Enter your message: ")
        arg = sys.stdin.read()
        data_type = "text"
    else:
        arg = " ".join(args.msg)
        data_type = _data_type(arg)

    _push(pb, channel, device, arg, data_type)

    return 0
