Pushbullet CLI interface
========================

Use [Pushbullet](https://www.pushbullet.com/) from the command line. In beta!

*Requires `requests` to be installed.*

You can clone this repo and then add the following to your bashrc (or your zshrc, or whatever):

    $ echo 'alias pushbullet="/path/to/pushbullet-cli/pushbullet.py'" >> ~/.bashrc
    $ source ~/.bashrc

Push stdin:
    $ echo "hello" | pushbullet [-a/-d/-i]

Push text:

    $ pushbullet [-a/-d/-i] burritos
    $ pushbullet [-a/-d/-i] "I love burritos"
    $ pushbullet [-a/-d/-i] Make sure you remember to eat a burrito

Push links:

    $ pushbullet [-a/-d/-i] http://losaltostaqueria.org/
    $ pushbullet [-a/-d/-i] https://www.pushbullet.com/

Push files:

    $ pushbullet [-a/-d/-i] /path/to/burrito_photo.jpg
    $ pushbullet [-a/-d/-i] /path/to/burrito_recipe.txt

Devices
-------
You should use one of the three flags -a, -d or -i to specify a device.
* -a will push to all devices.
* -d [name] will push to a specific device by name.
* -i will prompt you to choose to which device you want to push.

The first time you run this, you'll be asked for your API key, which will be saved in *~/.pushbulletkey*.

I'm not too experienced with Python, so please feel free to send a pull request!
