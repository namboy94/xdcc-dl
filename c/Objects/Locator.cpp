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