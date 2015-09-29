/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#include "Server.h"

//public
//Constructor

Server::Server(string name) {
    this->name = name;
}

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