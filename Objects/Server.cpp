/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#include "Server.h"

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

    channel.addToServer(this->);
    this->channels.push_back(channel);

}

//Getter/Setter

string Server::getName() {
    return this->name;
}

vector<Channel> Server::getChannels() {
    return this->channels;
}