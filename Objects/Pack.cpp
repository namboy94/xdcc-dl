/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#include "Pack.h"

//public
//Constructor

/**
 * Creates a new Pack object with a given pack number
 * @param packNumber - the number of the pack
 */
Pack::Pack(int packNumber) {

    this->packNumber = packNumber;

}

/**
 * adds this pack to a Bot.
 * @param bot - the bot to which this pack should be added.
 */
void Pack::addToBot(Bot bot) {

    this->bot = bot;

}

//getter/setter

Bot Pack::getBot() {
    return this->bot;
}

string Pack::getPackNumberString() {
    return "";
    //TODO return (string) this->packNumber;
}