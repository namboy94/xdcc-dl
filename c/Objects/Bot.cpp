/*
Copyright 2015-2017 Hermann Krumrey

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