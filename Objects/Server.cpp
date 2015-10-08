/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#include "ServerList.h"

//public
//Constructor

/**
 * Creates a new Server Object with an individual name
 * @param name - the name of the server
 */
Server::Server(string name) {
    this->name = name;
}

/**
 * Adds a channel to the server
 * @param channel - the channel to be added
 */
void Server::addChannel(Channel channel) {

    this->channels.push_back(channel);

}

/**
 * Adds a bot to an existing channel belonging to this server
 * @param bot - the bot to be added
 * @param channelIndex - the index of the channel to which the bot should be added
 */
void Server::addBot(Bot bot, int channelIndex) {

    this->channels[channelIndex].addBot(bot);

}

/**
 * Adds a pack to a bot that belongs to a channel that belongs to the server
 * @param pack - the pack to be added
 * @param channelIndex - the index of the channel to which the pack will be added
 * @param botIndex - the index of the bot to which the pack will be added
 */
void Server::addPack(Pack pack, int channelIndex, int botIndex){

    this->channels[channelIndex].addPack(pack, botIndex);

}

//Getter/Setter

string Server::getName() {
    return this->name;
}

vector<Channel> Server::getChannels() {
    return this->channels;
}