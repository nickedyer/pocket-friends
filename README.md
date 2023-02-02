
![Pocket Friends](https://github.com/nickedyer/pocket-friends/blob/master/pocket_friends/game_files/resources/images/promotional.png?raw=true)

[![License: GNU GPL v3.0](https://img.shields.io/badge/license-GNU%20GPL%20v3.0-blue)](LICENSE)

Pocket Friends is a game where you raise your own little pocket friend! These pocket friends, called bloops, are great little companions to have! You can feed them, play with them, and watch them grow up!

~~You can download the latest release of Pocket Friends on the [releases page.](https://github.com/nickedyer/pocket-friends/releases)~~
There are currently no releases of the game. To install the current version on GitHub, follow the instructions below.

---

## Installing From Source

Requirements:
- Python 3.10 or greater
- Pip
- Git

All you need to do to install Pocket Friends is install it with pip and you're good to go!

`pip install git+https://github.com/nickedyer/pocket-friends.git`

Now that the game is installed, just run it like you would any other Python program.

`python -m pocket_friends`

...and that's it! You now have the latest dev build of Pocket Friends installed on your system!

## Building for Windows

If you wish to build this version of Pocket Friends for Windows, you will need the same
requirements as to install it to your system from source. After you have done that,
issue the following:
```
git clone https://github.com/nickedyer/pocket-friends.git
cd pocket-friends
pip install -r requirements.txt
pip install pyinstaller
python compile.py
```
The compiled executable will then be in the `pocket-friends\dist` directory.