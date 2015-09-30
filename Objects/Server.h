/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#ifndef XDCC_DOWNLOAD_SERVER_H
#define XDCC_DOWNLOAD_SERVER_H

#include "Channel.h"

#include <string>
#include <vector>

using namespace std;

/**
 * Class that models an IRC server
 */
class Server{

public:

    //Constructor
    Server(string name);

    //Functional Functions
    void addChannel(Channel channel);

    //Getter/Setter
    string getName();
    vector<Channel> getChannels();


private:

    //local variables
    string name;
    vector<Channel> channels;

};

#endif //XDCC_DOWNLOAD_SERVER_H
