/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#include "Pack.h"

//public
//Constructor

Pack::Pack(int packNumber) {

    this->packNumber = packNumber;

}

void Pack::addToBot(Bot bot) {

    this->bot = bot;

}

Bot Pack::getBot() {

    return this->bot;

}

string Pack::getPackNumberString() {

    return "";
    //return (string) this->packNumber;

}