/**
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#include <iostream>
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
    this->textEditor = config.getTextEditor();

    parseFiles();

}

/**
 * Loads the server config with a single pack
 * @param config - the configuration to be used
 * @param packString - the pack to be loaded
 */
ServerList::ServerList(Config config, string packString) {

    cout << "start";

    this->serverFile = config.getServerFile();

    parseServerFile();

    istringstream parser(packString);

    string bot;
    string packNumberString;
    string throwAway;

    parser >> throwAway;
    parser >> bot;
    parser >> throwAway;
    parser >> throwAway;
    parser >> packNumberString;
    packNumberString.erase(0, 1);

    int packNumber;
    stringstream(packNumberString) >> packNumber;

    Pack pack(packNumber);

    addPack(pack, bot);

}

/**
 * Parses the server- and pack files in the correct order to minimize programming errors.
 */
void ServerList::parseFiles() {

    parseServerFile();
    parsePackFile();

}

//Getter/Setter

vector<Server> ServerList::getServers() {
    return this->servers;
}

//Finder Functions

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

void ServerList::refresh() {

    parseFiles();

}

void ServerList::serverEdit() {

    string command = this->textEditor + " " + this->serverFile;
    system(command.c_str());
    refresh();

}

void ServerList::packEdit() {

    string command = this->textEditor + " " + this->packFile;
    system(command.c_str());
    refresh();

}

void ServerList::addSingleBot(string botString) {

    appendLine(botString, this->serverFile);
    refresh();

}

void ServerList::addSinglePack(string packString) {

    appendLine(packString, this->packFile);

}

//private
//helper functions

/**
 * Parses the server file and loads all relevant data into the data structure
 */
void ServerList::parseServerFile() {

    vector<string> content = readFileNoHash(this->serverFile);

    for (int i = 0; i < content.size(); i++) {
        string line = content[i];

        if (regex_match(line, regex("(\\S)+ @ (\\S)+/(\\S)+"))) {

            istringstream parseStream(line);

            string server;
            string throwAway;
            string channelServer;
            string channel;
            string bot;

            parseStream >> bot;
            parseStream >> throwAway;
            parseStream >> channelServer;

            int slashPos = channelServer.find("/");
            string channelServerBackup = channelServer;

            server = channelServer.replace(slashPos, channelServer.size(), "");
            channel = channelServerBackup.replace(0, slashPos + 1, "");

            Server serverO(server);
            Channel channelO(channel);
            Bot botO(bot);

            int serverPos = find(serverO, this->servers);

            if (serverPos == -1) {
                channelO.addBot(botO);
                serverO.addChannel(channelO);
                this->servers.push_back(serverO);
            } else {
                vector<Channel> channels = this->servers[serverPos].getChannels();
                int channelPos = find(channelO, channels);
                if (channelPos == -1) {
                    channelO.addBot(botO);
                    this->servers[serverPos].addChannel(channelO);
                } else {
                    vector<Bot> bots = channels[channelPos].getBots();
                    int botPos = find(botO, bots);
                    if (botPos == -1) {
                        this->servers[serverPos].addBot(botO, channelPos);
                    }
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
        string line = content[i];

        if (regex_match(line, regex("/msg (\\S)+ xdcc send #[0-9]+"))) {

            istringstream parseStream(line);

            string bot;
            string pack;
            string throwAway;

            parseStream >> throwAway;
            parseStream >> bot;
            parseStream >> throwAway;
            parseStream >> throwAway;
            parseStream >> pack;
            pack.erase(0, 1);

            int packNumber;
            stringstream(pack) >> packNumber;

            Pack packO(packNumber);
            addPack(packO, bot);

            prevBot = bot;
            prevPack = packNumber;
        } else if (regex_match(line, regex("...[0-9]+"))) {
            string jumpVariable = line.replace(0, 3, "");
            int jumpVar;
            stringstream(jumpVariable) >> jumpVar;
            i++;

            if (regex_match(content[i], regex("/msg (\\S)+ xdcc send #[0-9]+"))) {

                istringstream parseStream(content[i]);

                string throwAway;
                string lastPackString;
                int lastPack;

                parseStream >> throwAway;
                parseStream >> throwAway;
                parseStream >> throwAway;
                parseStream >> throwAway;
                parseStream >> lastPackString;
                lastPackString.erase(0, 1);
                stringstream(lastPackString) >> lastPack;

                for (int j = prevPack + jumpVar; j <= lastPack; j += jumpVar) {
                    Pack currentPack(j);
                    addPack(currentPack, prevBot);
                }
            }
        }
    }
}

/**
 * Adds a pack to a bot
 * @param pack - the pack to be added
 * @param bot - the bot to which the pack should be added
 */
void ServerList::addPack(Pack pack, Bot bot) {

    Locator locate = find(bot);
    this->servers[locate.server].addPack(pack, locate.channel, locate.bot);
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