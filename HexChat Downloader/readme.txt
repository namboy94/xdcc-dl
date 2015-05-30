HexChat Downloader

This program automatically downloads packs via XDCC over IRC networks. The input is primarily based on parsing input files included
with the program. These can be edited via the command line interface via 'edit servers' or 'edit packs'
The program also features an advanced logging functionality, including sending logs via email.

The config.ini file has to be customized by the user. It has to contain the following parameters:

email sender = X
email receiver = X
email server = X
email port = X
email password = X
email active = true/false
text editor = X


Notes for Windows users:

This program is bundled with a 64 bit version of HexChat, so there's no need to manually install hexchat.
The only thing required to use this program is python 2.7. It should also work with 3+, this is however untested.

The first time this program is run, hexchat will open. You will need to configure the settings to your liking,
in particular the file transfer settings. It is recommended that you allow downloading without user prompts.
Showing server list on startup is also discouraged.



Notes for Linux users:

You need to have hexchat installed on your system, as well as the python plugin module for hexchat.