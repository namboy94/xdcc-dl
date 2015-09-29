/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#ifndef XDCC_DOWNLOAD_PACK_H
#define XDCC_DOWNLOAD_PACK_H

#include "Bot.h"

#include <string>
#include <vector>

using namespace std;

class Pack{

public:

    //Constructor
    Pack(int packNumber);

    void addToBot(Bot bot);

    string getPackNumberString();
    Bot getBot();


private:

    int packNumber;
    Bot bot = nullptr;

};

#endif //XDCC_DOWNLOAD_PACK_H
