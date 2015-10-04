#include <iostream>
#include "Objects/Config.h"
#include "Objects/ServerList.h"
#include "Downloaders/HexChatPythonDownloader.h"
#include "Interface/CLI.h"

using namespace std;

int main() {

    //Currently not portable, so linux-only

    Config config("/home/" + string(getenv("USER")) + "/.xdcc-download/files/config");
    ServerList serverList(config);
    HexChatPythonDownloader downloader(config, serverList);
    CLI cli(downloader, config);
    cli.mainLoop();

    return 0;
}