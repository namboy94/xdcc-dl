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
    string prevBot;
    int prevPack;

    for (int i = 0; i < content.size(); i++) {
        //Format: /msg tlacatlc6|XDCC xdcc send #884
        //TODO split into string for bot and packnumber
        //TODO Regex Match

        if (true) {
            string bot = "";
            string pack = "";
            //TODO cast string to int
            //int packNumber = (int) pack;
            int packNumber = 0;
            Pack packO(packNumber);
            addPack(packO, bot);

            prevBot = bot;
            prevPack = packNumber;
        } else if (true) {
            //TODO regex match for ...x
            string jumpVariable = content[i].replace(0, 3, "");
            //TODO cast to int
            int jumpVarInt = 0;

            i++;

            //Split packnumber of content[i];
            int lastPack = 0;

            for (int j = prevPack; j <= lastPack; j += jumpVarInt) {
                Pack currentPack(j);
                addPack(currentPack, prevBot);
            }
        }
    }
}










//private

ServerList::Locator::Locator(int server, int channel, int bot) {

    this->server = server;
    this->channel = channel;
    this->bot = bot;

}


void ServerList::addPack(Pack pack, Bot bot) {

    Locator locate = find(bot);
    this->servers[locate.server].getChannels()[locate.channel].getBots()[locate.bot].getPacks().push_back(pack);

}


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

Locator ServerList::find(Bot bot) {
    for (int i = 0; i < this->servers.size(); i++) {
        for (int j = 0; j < this->servers[i].getChannels().size(); j++) {
            for (int k = 0; k < this->servers[i].getChannels()[j].getBots().size(); k++) {
                if (!strcmp(this->servers[i].getChannels()[j].getBots()[k].getName().c_str(), bot.getName().c_str())) {
                    Locator locate(i, j, k);
                    return locate;
                }
            }
        }
    }
    Locator locate(-1, -1, -1);
    return locate;
}