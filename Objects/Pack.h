/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#ifndef XDCC_DOWNLOAD_PACK_H
#define XDCC_DOWNLOAD_PACK_H

#include "Bot.h"

#include <string>
#include <vector>

using namespace std;

/**
 * Models an XDCC pack
 */
class Pack{

public:

    //Constructor
    Pack(int packNumber);

    //Functional Functions
    void addToBot(Bot bot);

    //Getter/Setter
    string getPackNumberString();
    Bot getBot();


private:

    //private variables
    int packNumber;
    Bot bot = nullptr;

};

#endif //XDCC_DOWNLOAD_PACK_H
