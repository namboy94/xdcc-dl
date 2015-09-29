/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#include "ServerList.h"

#include "../Helpers/fileHandlers.h"

//public
//Constructor

/**
 * Loads relevant information from the config object and parses servers and packs
 * @param config - the configuration to be used
 */
ServerList::ServerList(Config config) {

    this->serverFile = config.getServerFile();
    this->packFile = config.getPackFile();

    parseServerFile();
    parsePackFile();

}

void ServerList::parseServerFile() {

    vector<string> content = readFileNoHash(this->serverFile);

    for (int i = 0; i < content.size(); i++) {
        //Format: Ginpachi-Sensei @ rizon/horriblesubs
        //TODO split into strings for bot, channel, server

        //TODO Regex Match

        string server ="";
        string channel ="";
        string bot ="";
        Server serverO(server);
        Channel channelO(channel);
        Bot botO(bot);
        channelO.addBot(botO);
        serverO.addChannel(channelO);

        int serverPos = find(serverO, this->servers);

        if (serverPos == -1) {
            this->servers.push_back(serverO);
        } else {
            vector<Channel> channels = this->servers[serverPos].getChannels();
            int channelPos = find(channelO, channels);
            if (channelPos == -1) {
                this->servers[serverPos].getChannels().push_back(channelO);
            } else {
                vector<Bot> bots = channels[channelPos].getBots();
                int botPos = find(botO, bots);
                if (botPos == -1) {
                    this->servers[serverPos].getChannels()[channelPos].getBots().push_back;
                }
            }
        }
    }
}

void ServerList::parsePackFile() {

    vector<string> content = readFileNoHash(this->packFile);
    string lastBot;
    int lastPack;

    for (int i = 0; i < content.size(); i++) {
        //Format: /msg tlacatlc6|XDCC xdcc send #884
        //TODO split into string for bot and packnumber
        //TODO Regex Match

        string bot = "";
        string pack = "";
        //TODO cast string to int
        //int packNumber = (int) pack;
        int packNumber = 0;

    }


}










//private

int ServerList::find(Server server, vector<Server> serverArray) {

    for (int i = 0; i < serverArray.size(); i++) {
        if (!strcmp(serverArray[i].getName().c_str(), server.getName().c_str())) {
            return i;
        }
    }
    return -1;

}

int ServerList::find(Channel channel, vector<Channel> channelArray) {

    for (int i = 0; i < channelArray.size(); i++) {
        if (!strcmp(channelArray[i].getName().c_str(), channel.getName().c_str())) {
            return i;
        }
    }
    return -1;

}

int ServerList::find(Bot bot, vector<Bot> botArray) {

    for (int i = 0; i < botArray.size(); i++) {
        if (!strcmp(botArray[i].getName().c_str(), bot.getName().c_str())) {
            return i;
        }
    }
    return -1;

}