# HexChat Downloader [![pipeline status](https://gitlab.namibsun.net/namboy94/hexchat-downloader/badges/master/pipeline.svg)](https://gitlab.namibsun.net/namboy94/hexchat-downloader/commits/master)

![Logo](resources/logo/logo-readme.png)

Note that this Program has been abandoned in favor of
[xdcc-dl](https://gitlab.namibsun.net/namboy94/xdcc-dl).

This program automatically downloads packs via XDCC over IRC networks.
The input is primarily based on parsing input files included
with the program.
These can be edited via the command line interface via 'edit servers' or
'edit packs'.
The program also features an advanced logging functionality,
including sending logs via email.

The config.ini file has to be customized by the user.
It has to contain the following parameters:

email sender = X
email receiver = X
email server = X
email port = X
email password = X
email active = true/false
text editor = X

## Notes for Windows users:

This program is bundled with a 64 bit version of HexChat,
so there's no need to manually install hexchat.
The only thing required to use this program is python 2.7.
It should also work with 3+, this is however untested.

The first time this program is run, hexchat will open.
You will need to configure the settings to your liking,
in particular the file transfer settings.
It is recommended that you allow downloading without user prompts.
Showing server list on startup is also discouraged.


## Notes for Linux users:

You need to have hexchat installed on your system,
as well as the python plugin module for hexchat.

## Further Information

* [Changelog](https://gitlab.namibsun.net/namboy94/hexchat-downloader/raw/master/CHANGELOG)
* [License (GPLv3)](https://gitlab.namibsun.net/namboy94/hexchat-downloader/raw/master/LICENSE)
* [Gitlab](https://gitlab.namibsun.net/namboy94/hexchat-downloader)
* [Github](https://github.com/namboy94/hexchat-downloader)
* [Git Statistics (gitstats)](https://gitstats.namibsun.net/gitstats/hexchat-downloader/index.html)
* [Git Statistics (git_stats)](https://gitstats.namibsun.net/git_stats/hexchat-downloader/index.html)
