/**
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#include <iostream>
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

    download(this->serverList[0]);

}

void HexChatPythonDownloader::refresh() {

    this->serverList[0].refresh();

}

void HexChatPythonDownloader::addSinglePack(string addPackString) {

    string packString = addPackString.erase(0, 4);
    this->serverList[0].addSinglePack(packString);

}

void HexChatPythonDownloader::addSingleBot(string addBotString) {

    string botString = addBotString.erase(0, 4);
    this->serverList[0].addSingleBot(botString);

}

void HexChatPythonDownloader::editPacks() {

    this->serverList[0].packEdit();

}

void HexChatPythonDownloader::editServers() {

    this->serverList[0].serverEdit();

}

void HexChatPythonDownloader::downloadSinglePack(string packString) {

    ServerList tempList(this->config[0], packString);
    download(tempList);

}

//private

void HexChatPythonDownloader::download(ServerList serverList) {

    vector<string> script;
    for (int i = 0; i < this->scriptStart.size(); i++) {
        script.push_back(this->scriptStart[i]);
    }

    vector<Server> servers = serverList.getServers();
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

    for (int i = 0; i < this->scriptEnd.size(); i++) {
        script.push_back(this->scriptEnd[i]);
    }

    writeToFile("/home/hermann/.config/hexchat/addons/xdccscript.py", script);

    system("hexchat");

}