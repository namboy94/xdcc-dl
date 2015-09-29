/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */
#include "Channel.h"

//public
//Constructor

Channel::Channel(string name) {

    this->name = name;

}

void Channel::addBot(Bot bot) {

    bot.addToChannel(this->);
    this->bots.push_back(bot);

}

void Channel::addToServer(Server server) {

    this->server = server;

}

//Getter/Setter

string Channel::getName() {

    return this->name;

}

vector<Bot> Channel::getBots() {

    return this->bots;

}

Server Channel::getServer() {

    return this->server;

}