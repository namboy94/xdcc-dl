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

/**
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#include "ServerList.h"


/**
 * Constructor for the Locator class
 * @param server - the array id of the server
 * @param channel - the array id of the channel
 * @param bot - the array id of the bot
 */
Locator::Locator(int server, int channel, int bot) {

    this->server = server;
    this->channel = channel;
    this->bot = bot;

}