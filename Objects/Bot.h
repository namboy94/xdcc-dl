/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#ifndef XDCC_DOWNLOAD_BOT_H
#define XDCC_DOWNLOAD_BOT_H

#include "Channel.h"
#include "Pack.h"

#include <string>
#include <vector>

using namespace std;

/**
 * Models an XDCC bot
 */
class Bot{

public:

    //Constructor
    Bot(string name);

    //Functional Functions
    void addPack(Pack pack);
    void addToChannel(Channel channel);

    //Getter/Setter
    string getName();
    vector<Pack> getPacks();
    Channel getChannel();


private:

    //private variables
    string name;
    vector<Pack> packs;
    Channel channel = nullptr;

};

#endif //XDCC_DOWNLOAD_BOT_H
