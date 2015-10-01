/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */
#include "ServerList.h"


//public
//Constructor

/**
 * Creates a new Bot object with a given name
 * @param name - the name of the bot
 */
Bot::Bot(string name) {

    this->name = name;

}

/**
 * Adds this bot to a given channel
 * @param channel - the channel to which this bot is to be added
 */
void Bot::addToChannel(Channel channel) {

    this->channel.push_back(channel);

}

/**
 * Adds a pack to this bot
 * @param pack - the pack to be added
 */
void Bot::addPack(Pack pack) {

    pack.addToBot(*this);
    this->packs.push_back(pack);

}


//Getter/Setter

string Bot::getName() {
    return this->name;
}

vector<Pack> Bot::getPacks() {
    return this->packs;
}

Channel Bot::getChannel() {
    return this->channel[0];
}