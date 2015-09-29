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

class Bot{

public:

    //Constructor
    Bot(string name);

    void addPack(Pack pack);
    void addToChannel(Channel channel);

    string getName();
    vector<Pack> getPacks();


private:

    string name;
    vector<Pack> packs;
    Channel channel;

};

#endif //XDCC_DOWNLOAD_BOT_H
