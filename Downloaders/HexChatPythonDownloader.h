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
    vector<string> scriptStart;
    vector<string> scriptEnd;

    //helper functions
    void variableInit();

};

#endif //XDCC_DOWNLOAD_HEXCHATPYTHONDOWNLOADER_H
