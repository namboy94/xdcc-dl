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
 * Adds a pack to this bot
 * @param pack - the pack to be added
 */
void Bot::addPack(Pack pack) {

    this->packs.push_back(pack);

}


//Getter/Setter

string Bot::getName() {
    return this->name;
}

vector<Pack> Bot::getPacks() {
    return this->packs;
}