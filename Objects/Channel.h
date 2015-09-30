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

/**
 * Class that models an IRC Channel
 */
class Channel{

public:

    //Constructor
    Channel(string name);

    //Functional Functions
    void addBot(Bot bot);
    void addToServer(Server server);

    //Getter/Setter
    string getName();
    vector<Bot> getBots();
    Server getServer();


private:

    //Local Variables
    string name;
    vector<Bot> bots;
    Server server = nullptr; //TODO Figure out how to use null like in java, if possible

};

#endif //XDCC_DOWNLOAD_CHANNEL_H
