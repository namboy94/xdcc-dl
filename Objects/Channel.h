/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#ifndef XDCC_DOWNLOAD_CHANNEL_H
#define XDCC_DOWNLOAD_CHANNEL_H

#include "Server.h"
#include "Bot.h"

#include <string>
#include <vector>

using namespace std;

class Channel{

public:

    //Constructor
    Channel(string name);

    void addBot(Bot bot);
    void addToServer(Server server);

    string getName();
    vector<Bot> getBots();
    Server getServer();


private:

    string name;
    vector<Bot> bots;
    Server server = nullptr;

};

#endif //XDCC_DOWNLOAD_CHANNEL_H
