Pushbullet CLI interface
========================

Use [Pushbullet](https://www.pushbullet.com/) from the command line. In beta!

*Requires `requests` to be installed.*  
*Requires `pip` to be installed.*

Install the package by typing `./setup.py install`. This will install the package in your current Python environment. 
Alternatively, you can also use `./setup.py develop` in order to install the package in develop mode, which means that the installed file is linked to the source tree.

Push stdin to all devices:

    $ echo "hello" | pb

Push text to all devices:

    $ pb burritos
    $ pb -a "I love burritos"

Pick a device to push to:

    $ pb -d "iPhone" iPhones cannot eat burritos

Interactively decide which device:

    $ pb -i Make sure you remember to eat a burrito

Push links:

    $ pb [-a/-d/-i] http://losaltostaqueria.org/
    $ pb [-a/-d/-i] https://www.pushbullet.com/

Push files:

    $ pb [-a/-d/-i] /path/to/burrito_photo.jpg
    $ pb [-a/-d/-i] /path/to/burrito_recipe.txt

Push to all subscribers of channel:

    $ pb -c "CHANNEL" Why burritos are better than tacos

Devices
-------

You should use one of the three flags -a, -d or -i to specify a device.

* -a will push to all devices.
* -d [name] will push to a specific device by name.
* -i will prompt you to choose to which device you want to push.
* -c [name] will push to a specific channel by name.

The first time you run this, you'll be asked for your API key, which will be saved in *~/.pushbulletkey*.
