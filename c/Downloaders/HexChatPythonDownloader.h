/*
Copyright 2015-2017 Hermann Krumrey <hermann@krumreyh.com>

This file is part of xdcc-downloader.

xdcc-downloader is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

xdcc-downloader is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with xdcc-downloader.  If not, see <http://www.gnu.org/licenses/>.
*/

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
