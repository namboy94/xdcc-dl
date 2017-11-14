/**
 * @author Hermann Krumrey <hermann@krumreyh.com>
 *
 * XDCC-Download is a program which automatically downloads a list of XDCC packs via IRC.
 * It allows the user to input the list as direct commands or for more advanced usage via a
 * input file providing the information for the packs to be downloaded
 */

#ifdef _WIN32
#include <windows>
#endif

#include <iostream>
#include "Objects/Config.h"
#include "Objects/ServerList.h"
#include "Downloaders/HexChatPythonDownloader.h"
#include "Interface/CLI.h"

/**
 * The Main Function that runs the program
 */
int main() {

    //TODO: GUI/CLI choice

#ifdef __linux__
    Config config("/home/" + string(getenv("USER")) + "/.xdcc-download/files/config");
#elif _WIN32
    //TODO: Windows Implementation
#endif

    ServerList serverList(config);
    HexChatPythonDownloader downloader(config, serverList);
    CLI cli(downloader, config);
    cli.mainLoop();

    return 0;
}