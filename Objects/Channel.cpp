/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */
#include "ServerList.h"

//public
//Constructor

/**
 * Creates a new Channel Object with a given name
 * @param name - the name of the channel
 */
Channel::Channel(string name) {

    this->name = name;

}

/**
 * Adds a bot to the channel
 * @param bot - the bot to be added
 */
void Channel::addBot(Bot bot) {

    bot.addToChannel(*this);
    this->bots.push_back(bot);

}

/**
 * Adds this channel to a server
 * @param server - the server to which this channel should be added to
 */
void Channel::addToServer(Server server) {

    this->server.push_back(server);

}

//Getter/Setter

string Channel::getName() {
    return this->name;
}

vector<Bot> Channel::getBots() {
    return this->bots;
}

Server Channel::getServer() {
    return this->server[0];
}