/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#ifndef XDCC_DOWNLOAD_SERVERLIST_H
#define XDCC_DOWNLOAD_SERVERLIST_H

//Personal Includes
#include "Config.h"
#include "Server.h"
#include "Channel.h"
#include "Bot.h"
#include "Pack.h"

//Standard Includes
#include <vector>

/*
 * Data Structure that keeps track of IRC servers and channels as well as XDCC bot and packs
 */
class ServerList{

public:

    //Constructor
    ServerList(Config config);

    //functional functions
    void parseFiles();
    void addPack(string downloadstring);

private:

    //private variables
    vector<Server> servers;
    string packFile;
    string serverFile;

    //helper functions
    void addPack(Pack pack, Bot bot);
    Pack createPackFromString(string packString);
    void parseServerFile();
    void parsePackFile();

    int find(Server server, vector<Server> serverArray);
    int find(Channel channel, vector<Channel> channelArray);
    int find(Bot bot, vector<Bot> botArray);
    Locator find(Bot bot);

    //extra class for traversing the structure
    class Locator {
    public:
        int server;
        int channel;
        int bot;
        Locator(int server, int channel, int bot);
    };
};

#endif //XDCC_DOWNLOAD_SERVERLIST_H
