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

    this->bots.push_back(bot);

}

void Channel::addPack(Pack pack, int botIndex) {

    this->bots[botIndex].addPack(pack);

}

//Getter/Setter

string Channel::getName() {
    return this->name;
}

vector<Bot> Channel::getBots() {
    return this->bots;
}