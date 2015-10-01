/**
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#include "HexChatPythonDownloader.h"

/**
 * Creates a new HexChatPythonDownloader
 */
HexChatPythonDownloader::HexChatPythonDownloader(Config config, ServerList serverList) {

    this->config.push_back(config);
    this->serverList.push_back(serverList);

}

/**
 * Creates a script to download all packs saved in the server list data structure
 */
void HexChatPythonDownloader::downloadAll() {

    vector<string> script;
    //script.push_back(this->scriptStart);

    vector<Server> servers = this->serverList[0].getServers();
    for (int i = 0; i < servers.size(); i++) {
        vector<Channel> channels = servers[i].getChannels();
        for (int j = 0; j < channels.size(); j++) {
            vector<Bot> bots = channels[j].getBots();
            for (int k = 0; k < bots.size(); k++) {
                vector<Pack> packs = bots[k].getPacks();
                for (int l = 0; l < packs.size(); l++) {
                    script.push_back("channels.append(\"newserver irc://" + servers[i].getName()
                                     + "/" + channels[j].getName() + "\")\n");
                    script.push_back("packs.append(\"msg " + bots[k].getName()
                                     + " xdcc send #" + packs[l].getPackNumberString() + "\")\n");
                }
            }
        }
    }

    //script.push_back(this->scriptEnd);

    writeToFile("/home/hermann/.config/hexchat/addons/xdccscript.py", script);

    system("hexchat");

}