/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#ifndef XDCC_DOWNLOAD_SERVER_H
#define XDCC_DOWNLOAD_SERVER_H

#include "Channel.h"

#include <string>
#include <vector>

using namespace std;

class Server{

public:

    //Constructor
    Server(string name);

    void addChannel(Channel channel);

    string getName();
    vector<Channel> getChannels();


private:

    string name;
    vector<Channel> channels;

};

#endif //XDCC_DOWNLOAD_SERVER_H
