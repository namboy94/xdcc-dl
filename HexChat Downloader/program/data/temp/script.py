

__module_name__ = "xdcc_executer"
__module_version__ = "0.1"
__module_description__ = "Python XDCC Executer"

import hexchat

def quitChannel(word, word_eol, userdata):
	hexchat.command('quit')
	packCounter += 1
	return hexchat.EAT-HEXCHAT

hexchat.hook_print("DCC RECV Complete", quitChannel)

packCounter = 0

def join_6336(word, word_eol, userdata):
	hexchat.command('msg Doki|Homura xdcc send #6336')
	return hexchat.EAT_HEXCHAT

hexchat.command('newserver irc://rizon/doki')
if packCounter == 0:
	hexchat.hook_print("You Join", join_6336)

def join_1237(word, word_eol, userdata):
	hexchat.command('msg Doki|Kyou xdcc send #1237')
	return hexchat.EAT_HEXCHAT

hexchat.command('newserver irc://rizon/doki')
if packCounter == 1:
	hexchat.hook_print("You Join", join_1237)

