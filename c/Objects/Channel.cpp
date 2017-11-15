/*
Copyright 2015-2017 Hermann Krumrey <hermann@krumreyh.com>

This file is part of xdcc-downloader.

xdcc-downloader is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

xdcc-downloader is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with xdcc-downloader.  If not, see <http://www.gnu.org/licenses/>.
*/

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

/**
 * Adds a pack to a bot belonging to the channel
 * @param pack - the pack to be added
 * @param botIndex - the index of the bot to which this pack should be added
 */
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