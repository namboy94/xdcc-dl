/*
Copyright 2015-2017 Hermann Krumrey <hermann@krumreyh.com>

This file is part of xdcc-downloader.

xdcc-downloader is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

xdcc-downloader is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with xdcc-downloader.  If not, see <http://www.gnu.org/licenses/>.
*/

/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 * Collection of classes necessary for the implementation of the ServerList Data Structure
 */

#ifndef XDCC_DOWNLOAD_SERVERLIST_H
#define XDCC_DOWNLOAD_SERVERLIST_H

#include "Config.h"
#include <vector>
#include <regex>
#include <sstream>

class Server;
class Channel;
class Bot;
class Pack;
class Locator;


/*
 * Data Structure that keeps track of IRC servers and channels as well as XDCC bot and packs
 */
class ServerList{

public:

    //Constructor
    ServerList(Config config);
    ServerList(Config config, string packString);

    //functional functions
    void parseFiles();

    void refresh();

    void packEdit();

    void serverEdit();

    void addSinglePack(string packString);

    void addSingleBot(string botString);

    //Getter/Setter
    vector<Server> getServers();

    //public helper functions
    int find(Server server, vector<Server> serverArray);
    int find(Channel channel, vector<Channel> channelArray);
    int find(Bot bot, vector<Bot> botArray);

private:

    //private variables
    vector<Server> servers;
    string packFile;
    string serverFile;
    string textEditor;

    //helper functions
    void addPack(Pack pack, Bot bot);
    void parseServerFile();
    void parsePackFile();

    Locator find(Bot bot);
};

/**
 * Class that saves the location of a bot or pack in the data structure
 */
class Locator {
public:
    int server;
    int channel;
    int bot;
    Locator(int server, int channel, int bot);
};

/**
 * Class that models an IRC server
 */
class Server{

public:

    //Constructor
    Server(string name);

    //Functional Functions
    void addChannel(Channel channel);
    void addBot(Bot bot, int channelIndex);
    void addPack(Pack pack, int channelIndex, int botIndex);

    //Getter/Setter
    string getName();
    vector<Channel> getChannels();


private:

    //local variables
    string name;
    vector<Channel> channels;
};




/**
 * Class that models an IRC Channel
 */
class Channel{

public:

    //Constructor
    Channel(string name);

    //Functional Functions
    void addBot(Bot bot);
    void addPack(Pack pack, int botIndex);

    //Getter/Setter
    string getName();
    vector<Bot> getBots();


private:

    //Local Variables
    string name;
    vector<Bot> bots;
};



/**
 * Models an XDCC bot
 */
class Bot {

public:

    //Constructor
    Bot(string name);

    //Functional Functions
    void addPack(Pack pack);

    //Getter/Setter
    string getName();
    vector<Pack> getPacks();


private:

    //private variables
    string name;
    vector<Pack> packs;
};



/**
 * Models an XDCC pack
 */
class Pack{

public:

    //Constructor
    Pack(int packNumber);

    //Getter/Setter
    string getPackNumberString();


private:

    //private variables
    int packNumber;

};

#endif //XDCC_DOWNLOAD_SERVERLIST_H