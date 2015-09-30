/**
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

    parseFiles();

}

/**
 * Parses the server- and pack files in the correct order to minimize programming errors.
 */
void ServerList::parseFiles() {

    parseServerFile();
    parsePackFile();

}

//private
//helper functions

/**
 * Parses the server file and loads all relevant data into the data structure
 */
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

/**
 * Parses the pack file and loads all relevant information into the data structure
 * Supports easy batches via jumping variables given in the format ...x
 */
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

/**
 * Constructor for the Locator class
 * @param server - the array id of the server
 * @param channel - the array id of the channel
 * @param bot - the array id of the bot
 */
ServerList::Locator::Locator(int server, int channel, int bot) {

    this->server = server;
    this->channel = channel;
    this->bot = bot;

}

/**
 * Adds a pack to a bot
 * @param pack - the pack to be added
 * @param bot - the bot to which the pack should be added
 */
void ServerList::addPack(Pack pack, Bot bot) {

    Locator locate = find(bot);
    this->servers[locate.server].getChannels()[locate.channel].getBots()[locate.bot].getPacks().push_back(pack);

}

/**
 * Searches an array of servers for one specific server and returns its position in the array
 * @param server - the server to be searched for
 * @param serverArray - the array of Servers to be searched in
 * @return the location of the Server in the array. If it's not in the array, -1
 */
int ServerList::find(Server server, vector<Server> serverArray) {

    for (int i = 0; i < serverArray.size(); i++) {
        if (!strcmp(serverArray[i].getName().c_str(), server.getName().c_str())) {
            return i;
        }
    }
    return -1;

}

/**
 * Searches an array of channels for one specific channel and returns its position in the array
 * @param channel - the server to be searched for
 * @param channelArray - the array of Channels to be searched in
 * @return the location of the Channel in the array. If it's not in the array, -1
 */
int ServerList::find(Channel channel, vector<Channel> channelArray) {

    for (int i = 0; i < channelArray.size(); i++) {
        if (!strcmp(channelArray[i].getName().c_str(), channel.getName().c_str())) {
            return i;
        }
    }
    return -1;

}

/**
 * Searches an array of botss for one specific bot and returns its position in the array
 * @param bot - the bot to be searched for
 * @param botArray - the array of Bots to be searched in
 * @return the location of the Bot in the array. If it's not in the array, -1
 */
int ServerList::find(Bot bot, vector<Bot> botArray) {

    for (int i = 0; i < botArray.size(); i++) {
        if (!strcmp(botArray[i].getName().c_str(), bot.getName().c_str())) {
            return i;
        }
    }
    return -1;

}

/**
 * Searches the data structure for a specific bot and returns its location in it as a Locator
 * @param bot - the bot to be searched for
 * @returns the location of the bot. If the bot does not exist, (-1, -1, -1)
 */
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