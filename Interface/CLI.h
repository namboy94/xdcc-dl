/**
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#ifndef XDCC_DOWNLOAD_CLI_H
#define XDCC_DOWNLOAD_CLI_H

#include "../Downloaders/HexChatPythonDownloader.h"

/**
 * Class that allows User Interaction via a command line interface
 */
class CLI {

public:

    //Constructor
    CLI(HexChatPythonDownloader downloader, Config config);

    //Functional functions
    void mainLoop();

private:

    //private variables
    vector<HexChatPythonDownloader> downloader;
    vector<Config> config;

    vector<string> helpString = {"List of Commands:\n\n",
                                 "\n\n"};

};

#endif //XDCC_DOWNLOAD_CLI_H
