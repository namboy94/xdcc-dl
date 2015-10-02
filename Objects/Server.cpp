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

void Server::addBot(Bot bot, int channelIndex) {

    this->channels[channelIndex].addBot(bot);

}

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