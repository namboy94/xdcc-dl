#include <iostream>
#include "Objects/Config.h"
#include "Helpers/fileHandlers.h"

using namespace std;

int main() {

    /**
     * Workflow
     *
     * First, Load and parse Config
     * then load server file
     * then load current pack file
     *
     * load gui or cli based on console parameters
     *
     * start user interaction
     * Options:
     *
     * Start Packfile Download
     * Edit Packfile -> reload
     * Edit Serverfile -> reload
     * Set up email logs
     * Start a single download
     * Quit
     */

    /**
     * Pseudo Code
     *
     * Object Config = new Config(configFile);
     * //Object Servers = new Servers(Config.serverFile)
     * Object Packs = new Packs(Config.packFile, Servers/Config)
     *
     * if cli start CLI else start gui
     * loop{
     *
     * edit packs opens editor Config.editor(packfile) and updates on close
     * edit servers opens editor Config.editor(serverfile) and updates on close
     *
     * start download of packs in packfile
     *
     * download single parses a single user input pack and downloads it
     *
     * system.exit
     *
     * }
     */

    Config config("/home/hermann/Jetbrains/CLion/xdcc-download/Data/config");

    return 0;
}