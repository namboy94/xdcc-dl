/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */
#include "Bot.h"


//public
//Constructor

Bot::Bot(string name) {

    this->name = name;

}

void Bot::addToChannel(Channel channel) {

    this->channel = channel;

}

void Bot::addPack(Pack pack) {

    pack.addToBot(this->);
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

    return this->channel;

}