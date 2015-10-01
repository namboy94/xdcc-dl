/**
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#ifndef XDCC_DOWNLOAD_HEXCHATPYTHONDOWNLOADER_H
#define XDCC_DOWNLOAD_HEXCHATPYTHONDOWNLOADER_H

#include "../Objects/ServerList.h"
#include <vector>

/**
 * Class that handles downloading files through Hexchat via a generated python script
 */
class HexChatPythonDownloader{

public:

    //Constructor
    HexChatPythonDownloader(Config config, ServerList serverList);

    //Functional functions
    void downloadAll();


private:

    //private variables
    vector<string> scriptContent;
    vector<Config> config;
    vector<ServerList> serverList;

    vector<string> scriptStart = {  "__module_name__ = \"xdcc_executer\"\n",
                                    "__module_version__ = \"0.1\"\n",
                                    "import hexchat\n",
                                    "def download(word, word_eol, userdata):\n",
                                    "\thexchat.command(packs[0])\n",
                                    "\treturn hexchat.EAT_HEXCHAT\n",
                                    "def downloadComplete(word, word_eol, userdata):\n",
                                    "\thexchat.command('quit')\n",
                                    "\tchannels.pop(0)\n",
                                    "\tpacks.pop(0)\n",
                                    "\tif len(channels) == 0:\n",
                                    "\t\tsys.exit(1)\n",
                                    "\telse:\n",
                                    "\t\thexchat.command(channels[0])\n",
                                    "\treturn hexchat.EAT_HEXCHAT\n",
                                    "failed = []\n",
                                    "channels = []\n",
                                    "packs = []\n" };

    vector<string> scriptEnd = {    "hexchat.command(channels[0])\n",
                                    "hexchat.hook_print(\"You Join\", download)\n",
                                    "hexchat.hook_print(\"DCC RECV Complete\", downloadComplete)\n",
                                    "hexchat.hook_print(\"DCC STALL\", downloadFailed)\n",
                                    "hexchat.hook_print(\"DCC RECV Abort\", downloadFailed)\n",
                                    "hexchat.hook_print(\"DCC RECV Failed\", downloadFailed)\n",
                                    "hexchat.hook_print(\"DCC Timeout\", downloadFailed)\n" };

};

#endif //XDCC_DOWNLOAD_HEXCHATPYTHONDOWNLOADER_H
