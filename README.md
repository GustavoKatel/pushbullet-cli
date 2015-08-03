Pushbullet CLI interface
========================

Use [Pushbullet](https://www.pushbullet.com/) from the command line.

First of all, set your API key by running:

    $ pb set-key

Then pasting your API key at the prompt.

Push stdin to all devices:

    $ echo "hello" | pb push text

Push text to all devices:

    $ pb push text "I love burritos"

Pick a device to push to:

    $ pb list-devices
    # Find the index of your desired device
    $ pb push -d 0 text "iPhones cannot eat burritos"

Push links:

    $ pb push link https://www.pushbullet.com/

Push files:

    $ pb push file /path/to/burrito_photo.jpg

Push to all subscribers of channel:

    $ pb push -c "CHANNEL" text "Why burritos are better than tacos"
