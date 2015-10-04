/**
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#ifndef XDCC_DOWNLOAD_CLI_H
#define XDCC_DOWNLOAD_CLI_H

#include "../Downloaders/HexChatPythonDownloader.h"

class CLI {

public:

    CLI(HexChatPythonDownloader downloader, Config config);

    void mainLoop();

private:

    vector<HexChatPythonDownloader> downloader;
    vector<Config> config;

    vector<string> helpString = {"List of Commands:\n\n",
                                 "\n\n"};

};

#endif //XDCC_DOWNLOAD_CLI_H
