/**
 * @author Hermann Krumrey <hermann@krumreyh.com>
 *
 * XDCC-Download is a program which automatically downloads a list of XDCC packs via IRC.
 * It allows the user to input the list as direct commands or for more advanced usage via a
 * input file providing the information for the packs to be downloaded
 */

#include <iostream>
#include "Objects/Config.h"
#include "Objects/ServerList.h"
#include "Downloaders/HexChatPythonDownloader.h"
#include "Interface/CLI.h"

using namespace std;

/**
 * The Main Function that runs the program
 */
int main() {

    Config config("/home/" + string(getenv("USER")) + "/.xdcc-download/files/config");
    ServerList serverList(config);
    HexChatPythonDownloader downloader(config, serverList);
    CLI cli(downloader, config);
    cli.mainLoop();

    return 0;
}