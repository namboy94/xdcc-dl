/**
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#ifndef XDCC_DOWNLOAD_HEXCHATPYTHONDOWNLOADER_H
#define XDCC_DOWNLOAD_HEXCHATPYTHONDOWNLOADER_H

#include "../Objects/ServerList.h"
#include <vector>
#include "GenericDownloader.h"

/**
 * Class that handles downloading files through Hexchat via a generated python script
 */
class HexChatPythonDownloader : public GenericDownloader {

public:

    //Constructor
    HexChatPythonDownloader(Config config, ServerList serverList);

    //Functional functions
    void downloadAll();
    void addSinglePack(string addPackString);
    void addSingleBot(string addBotString);
    void downloadSinglePack(string packString);
    void editPacks();
    void editServers();
    void printAll();
    void printPacks();


private:

    //helper functions
    void download(ServerList serverList);

    void printMode(string mode);

    //private variables
    vector<string> scriptContent;
    vector<Config> config;
    vector<ServerList> serverList;

    vector<string> scriptStart = {"__module_name__ = \"xdcc_executer\"",
                                  "__module_version__ = \"0.1\"",
                                  "__module_description__ = \"Python XDCC Executer\"\n",
                                  "import hexchat",
                                  "import sys\n",
                                  "def download(word, word_eol, userdata):",
                                  "\thexchat.command(packs[0])",
                                    "\treturn hexchat.EAT_HEXCHAT\n",
                                  "def downloadComplete(word, word_eol, userdata):",
                                  "\thexchat.command('quit')",
                                  "\tchannels.pop(0)",
                                  "\tpacks.pop(0)",
                                  "\tif len(channels) == 0:",
                                  "\t\tsys.exit(1)",
                                  "\telse:",
                                  "\t\thexchat.command(channels[0])",
                                    "\treturn hexchat.EAT_HEXCHAT\n",
                                  "def downloadFailed(word, word_eol, userdata):",
                                  "\tfailed.append(packs[0])",
                                  "\thexchat.command('quit')",
                                  "\tchannels.pop(0)",
                                  "\tpacks.pop(0)",
                                  "\tif len(channels) == 0:",
                                  "\t\tsys.exit(1)",
                                  "\telse:",
                                  "\t\thexchat.command(channels[0])",
                                  "\treturn hexchat.EAT_HEXCHAT\n",
                                  "failed = []",
                                  "channels = []",
                                    "packs = []\n" };

    vector<string> scriptEnd = {"hexchat.command(channels[0])",
                                "hexchat.hook_print(\"You Join\", download)",
                                "hexchat.hook_print(\"DCC RECV Complete\", downloadComplete)",
                                "hexchat.hook_print(\"DCC STALL\", downloadFailed)",
                                "hexchat.hook_print(\"DCC RECV Abort\", downloadFailed)",
                                "hexchat.hook_print(\"DCC RECV Failed\", downloadFailed)",
                                "hexchat.hook_print(\"DCC Timeout\", downloadFailed)"};

};

#endif //XDCC_DOWNLOAD_HEXCHATPYTHONDOWNLOADER_H
