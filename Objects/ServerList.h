/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#ifndef XDCC_DOWNLOAD_SERVERLIST_H
#define XDCC_DOWNLOAD_SERVERLIST_H

#include "Config.h"
#include "Server.h"
#include "Channel.h"
#include "Bot.h"
#include "Pack.h"

#include <vector>

/*
 * Data Structure that keeps track of IRC servers and channels as well as XDCC bot and packs
 */
class ServerList{

public:

    //Constructor
    ServerList(Config config);

    void parseServerFile();
    void parsePackFile();
    void addPack(string downloadstring);

private:

    vector<Server> servers;
    string packFile;
    string serverFile;

    void addPack(Bot bot, Pack pack);
    Pack createPackFromString(string packString);

    int find(Server server, vector<Server> serverArray);
    int find(Channel channel, vector<Channel> channelArray);
    int find(Bot bot, vector<Bot> botArray);

    /*
    bool isInList(Server server);
    bool isInList(Channel channel);
    bool isInList(Bot bot);
     */


};

#endif //XDCC_DOWNLOAD_SERVERLIST_H
