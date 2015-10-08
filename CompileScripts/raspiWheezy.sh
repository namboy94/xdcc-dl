#!/bin/bash
#include all .h and .cpp files contained in CMakeLists.txt
#gcc version 4.9 has to be installed, via Debian Jessie's Repositories

MAIN="../main.cpp"
DOWNLOADERS="../Downloaders/GenericDownloader.h ../Downloaders/HexChatPythonDownloader.h ../Downloaders/HexChatPythonDownloader.cpp"
HELPERS="../Helpers/fileHandlers.h ../Helpers/fileHandlers.cpp"
INTERFACE="../Interface/CLI.h ../Interface/CLI.cpp"
OBJECTS="../Objects/Config.h ../Objects/Config.cpp ../Objects/ServerList.h ../Objects/ServerList.cpp ../Objects/Bot.cpp ../Objects/Channel.cpp ../Objects/Server.cpp ../Objects/Pack.cpp Locator.cpp"


g++-4.9 -std=c++0x $MAIN $DOWNLOADERS $HELPERS $INTERFACE $OBJECTS