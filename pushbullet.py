#! /usr/bin/env python

import argparse
import os.path
import requests

PUSH_URL = "https://api.pushbullet.com/api/pushes"

# utility methods
# ===============


def is_url(string):
    if " " in string:
        return False
    elif string[0:7] == "http://":
        return True
    elif string[0:8] == "https://":
        return True
    else:
        return False


def nickname_for(device):
    if not device:
        return "All"

    extras = device[u"extras"]
    if u"nickname" in extras:
        return extras[u"nickname"]
    else:
        return extras[u"model"]

parser = argparse.ArgumentParser(description='Pushbullet')
parser.add_argument('msg', metavar='message', nargs='+')

devgroup = parser.add_mutually_exclusive_group(required=True)
devgroup.add_argument('-a', '--all', default=False, action='store_true', help='Push to all devices')
devgroup.add_argument('-i', '--interactive', default=False, action='store_true',
                      help='Interactively ask for device to push to')
devgroup.add_argument('-d', '--device', type=str, default=None, help='Device name to push to')

args = parser.parse_args()

# get the API key
# ===============

key_path = os.path.expanduser("~/.pushbulletkey")
if not os.path.isfile(key_path):

    print("What's your API key?")
    print("Find it at <https://www.pushbullet.com/account>.")
    api_key = raw_input("> ").strip()
    with open(key_path, "w") as api_file:
        api_file.write(api_key)

else:

    api_key = open(key_path, "r").read().strip()

# get the list of devices
# =======================

r = requests.get("https://api.pushbullet.com/api/devices", auth=(api_key, ""))

if (r.status_code == 401) or (r.status_code == 403):
    print("Bad API key. Check " + key_path + ".")
    exit(1)

elif r.status_code != 200:
    print("Request failed with code " + str(r.status_code) + ".")
    print("Try again?")
    exit(1)

devices = r.json()[u"devices"]
devices_by_names = {d['extras']['model']: d for d in devices}

# pick the device to use
# ======================

push_to = None

if len(devices) < 1:
    print("You don't have any devices!")
    print("Add one at <https://www.pushbullet.com/>.")
    exit(1)

if args.interactive:
    for i in xrange(len(devices)):

        device = devices[i]
        nickname = nickname_for(device)
        index = str(i + 1)

        print("[" + index + "]"),
        print(nickname)

    while True:
        input = raw_input("Push to which device? ").strip()
        try:
            choice = int(input) - 1

        except (ValueError, IndexError):
            pass
        else:
            if 0 <= choice < len(devices):
                push_to = devices[choice]
                break


elif args.device:
    if args.device not in devices_by_names:
        print("Unknown device %s. Available devices: %s" % (
            args.device, ', '.join(devices_by_names)))
        exit(1)

    push_to = devices_by_names[args.device]

# push!
# =====

print("Pushing to " + nickname_for(push_to) + "...")

data = {}

if push_to:
    data["device_iden"] = push_to[u"iden"]

file = None

argument = " ".join(args.msg)

if is_url(argument):
    data["type"] = "link"
    data["title"] = "Link"
    data["url"] = argument
elif os.path.isfile(argument):
    data["type"] = "file"
    file = argument
else:
    data["type"] = "note"
    data["title"] = "Note"
    data["body"] = argument

r = None
if file is None:
    r = requests.post(
        PUSH_URL,
        auth=(api_key, ""),
        data=data
    )
else:
    r = requests.post(
        PUSH_URL,
        auth=(api_key, ""),
        data=data,
        files={"file": open(file, "rb")}
    )

if r.status_code == 200:
    print("Pushed!")
else:
    print("Failed with status code " + str(r.status_code) + ".")
    exit(1)
