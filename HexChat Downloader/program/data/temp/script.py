__module_name__ = "xdcc_executer"
__module_version__ = "0.1"
__module_description__ = "Python XDCC Executer"

import hexchat
import sys

def download(word, word_eol, userdata):
	hexchat.command(packs[0])
	return hexchat.EAT_HEXCHAT

def downloadComplete(word, word_eol, userdata):
	hexchat.command('quit')
	channels.pop(0)
	packs.pop(0)
	if len(channels) == 0:
		print "DOWNLOADS COMPLETE"
		sys.exit(1)
	else:
		hexchat.command(channels[0])
	return hexchat.EAT_HEXCHAT

def downloadFailed(word, word_eol, userdata):
	failed.append(packs[0])
	hexchat.command('quit')
	channels.pop(0)
	packs.pop(0)
	if len(channels) == 0:
		print "DOWNLOADS COMPLETE"
		sys.exit(1)
	else:
		hexchat.command(channels[0])
	return hexchat.EAT_HEXCHAT

failed = []
channels = []
packs = []

channels.append("newserver irc://rizon/test")
packs.append("msg TESTBOT xdcc send #12345")

hexchat.command(channels[0])
hexchat.hook_print("You Join", download)
hexchat.hook_print("DCC RECV Complete", downloadComplete)
hexchat.hook_print("DCC STALL", downloadFailed)
hexchat.hook_print("DCC RECV Abort", downloadFailed)
hexchat.hook_print("DCC RECV Failed", downloadFailed)
hexchat.hook_print("DCC Timeout", downloadFailed)

