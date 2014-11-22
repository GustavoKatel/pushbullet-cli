#!/usr/bin/env python

import argparse
import os.path
import requests
import re
import sys

PUSH_URL = "https://api.pushbullet.com/api/pushes"
DEVICE_URL = "https://api.pushbullet.com/api/devices"
KEY_PATH = os.path.expanduser("~/.pushbulletkey")
URL_RE = re.compile(r"^[a-zA-Z]+://.+$")


class PushbulletException(Exception):
    pass


def _nickname_for(device):
    if not device:
        return "all devices"

    extras = device[u"extras"]
    if u"nickname" in extras:
        return extras[u"nickname"]
    else:
        return extras[u"model"]


def _parse_args():
    parser = argparse.ArgumentParser(description='Pushbullet')
    parser.add_argument('msg', metavar='message', nargs='*')

    devgroup = parser.add_mutually_exclusive_group()
    devgroup.add_argument('-a', '--all', default=False, action='store_true',
                          help='Push to all devices')
    devgroup.add_argument('-i', '--interactive', default=False,
                          action='store_true',
                          help='Interactively ask for device to push to')
    devgroup.add_argument('-d', '--device', type=str, default=None,
                          help='Device name to push to')

    return parser.parse_args()


def _get_api_key():
    if not os.path.isfile(KEY_PATH):
        print("What's your API key?")
        print("Find it at <https://www.pushbullet.com/account>.")
        api_key = raw_input("> ").strip()
        with open(KEY_PATH, "w") as api_file:
            api_file.write(api_key)

        return api_key
    else:
        with open(KEY_PATH, "r") as api_file:
            return api_file.read()


def _get_devices(api_key):
    r = requests.get(DEVICE_URL, auth=(api_key, ""))
    if (r.status_code == 401) or (r.status_code == 403):
        raise PushbulletException("Bad API key. Check %s." % (KEY_PATH, ))
    elif r.status_code != 200:
        raise PushbulletException("Request failed with code %d." %
                                  (r.status_code, ))

    return r.json()[u"devices"]


def _prompt_device(devices):
    for i, device in enumerate(devices):
        nickname = _nickname_for(device)
        print ("[%d] %s" % (i, nickname))

    while True:
        input = raw_input("Push to which device? ").strip()
        try:
            choice = int(input)
        except (ValueError, IndexError):
            pass
        else:
            if 0 <= choice < len(devices):
                return devices[choice]


def _push(api_key, device, raw_data, data_type):
    data = {}

    if device:
        data["device_iden"] = device[u"iden"]

    kwargs = {
        'auth': (api_key, ""),
        'data': data
    }

    if data_type == 'url':
        data["type"] = "link"
        data["title"] = "Link"
        data["url"] = raw_data
    elif data_type == 'file':
        data["type"] = "file"
        kwargs['files'] = {'file': open(raw_data, 'rb')}
    elif data_type == 'text':
        data["type"] = "note"
        data["title"] = "Note"
        data["body"] = raw_data

    print("Pushing to %s..." % (_nickname_for(device), ))
    r = requests.post(PUSH_URL, **kwargs)

    if r.status_code != 200:
        raise PushbulletException("Failed with status code %d" %
                                  (r.status_code, ))


def _data_type(argument):
    if os.path.isfile(argument):
        return "file"
    elif URL_RE.search(argument):
        return "url"
    else:
        return "text"


def main():
    device = None
    args = _parse_args()

    api_key = _get_api_key()

    if not args.all:
        devices = _get_devices(api_key)

        if len(devices) < 1:
            print("You don't have any devices!")
            print("Add one at <https://www.pushbullet.com/>.")
            return 1

        if args.interactive:
            device = _prompt_device(devices)
        elif args.device:
            devices_by_names = {_nickname_for(d): d for d in devices}
            if args.device not in devices_by_names:
                print("Unknown device %s. Available devices: %s" % (
                    args.device, ', '.join(devices_by_names)))
                return 1
            device = devices_by_names[args.device]

    if not args.msg:
        arg = sys.stdin.read()
        data_type = 'text'
    else:
        arg = " ".join(args.msg)
        data_type = _data_type(arg)

    _push(api_key, device, arg, data_type)

    return 0
