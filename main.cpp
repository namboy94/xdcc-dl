#include <iostream>
#include "Objects/Config.h"
#include "Objects/ServerList.h"
#include "Downloaders/HexChatPythonDownloader.h"

using namespace std;

int main() {

    //Currently not portable, so linux-only

    /**
     * Workflow
     *
     * First, Load and parse Config - Done
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

    ServerList serverList(config);

    HexChatPythonDownloader downloader(config, serverList);
    downloader.downloadAll();

    vector<Server> servers = serverList.getServers();

    for (int i = 0; i < servers.size(); i++) {
        //cout << "\n" + servers[i].getName() + "\n";
        vector<Channel> channels = servers[i].getChannels();
        for (int j = 0; j < channels.size(); j++) {
            //cout << channels[j].getName() + "\n";
            vector<Bot> bots = channels[j].getBots();
            for (int k = 0; k < bots.size(); k++) {
                //cout << bots[k].getName() + "\n";
                vector<Pack> packs = bots[k].getPacks();
                for (int l = 0; l < packs.size(); l++) {
                    cout << packs[l].getPackNumberString() + " ";
                }
            }
        }
    }

    return 0;
}