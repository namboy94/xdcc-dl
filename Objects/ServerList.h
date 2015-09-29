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
    ServerList();

    void parseServerFile();
    void parsePackFile();
    void addPack(string downloadstring);

private:

    vector<Server> servers;

    void addServer(Server server);
    void addChannel(Channel channel);
    void addBot(Bot bot);
    void addPack(Pack pack);
    Pack createPackFromString();


};

#endif //XDCC_DOWNLOAD_SERVERLIST_H
